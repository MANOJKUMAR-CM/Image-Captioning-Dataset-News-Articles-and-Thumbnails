
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.filesystem import FileSensor

from datetime import datetime
from bs4 import BeautifulSoup

from Module1 import Scrape_HomePage
from Module2 import Scrape_TopStories
from Module3 import Extract_HeadLine_Thumbnail
from Module4 import Insert_headline, Insert_image, check
from Module5 import create_file

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 10),
    'retries': 1,
}


def AddData_to_DB(data):
    count = 0
    for image_path, headline in data:
        if not check(headline):
            image_id = Insert_image(image_path)
            Insert_headline(headline, image_id)
            count+=1
    return count # Returns the count of new Top stories added 

def Create_Status_File(ti): # Wrapper Function
    k = ti.xcom_pull(task_ids = "Add_Data_to_Tables") # get the count of stories added
    path = create_file(k)
    ti.xcom_push(key="file_path", value=path)

def Add_Data_to_DataBase(ti): # Wrapper Function 
    data =ti.xcom_pull(task_ids = "Extract_TopStories")
    print("Adding data to DataBase")
    c = AddData_to_DB(data)
    print("Finished Adding Data to DataBase")
    print("Number of Stories Added: ", c)
    
    return c
    
def Scrape_topstories(ti): # Wrapper Function
    s_html = ti.xcom_pull(task_ids = "Scrape_HomePage")
    #print(type(s_html)) -> <class 'str'>
    s = BeautifulSoup(s_html, 'html.parser')
    print("Scraping Top Stories Page")
    S = Scrape_TopStories(s)
    print("Scraping Completed.")
    return str(S)

def Extract_HeadlineThumbnail(ti): # Wrapper Function
    S_html = ti.xcom_pull(task_ids = "Scrape_TopStories")
    S = BeautifulSoup(S_html, 'html.parser')
    print("Extracting Process Begins")
    data = Extract_HeadLine_Thumbnail(S)
    
    return data
    

create_tables = """
    CREATE TABLE IF NOT EXISTS images (
        image_id SERIAL PRIMARY KEY,
        image_data BYTEA NOT NULL
    );

    CREATE TABLE IF NOT EXISTS headlines (
        headline_id SERIAL PRIMARY KEY,
        headline TEXT UNIQUE NOT NULL,
        image_id INTEGER REFERENCES images(image_id) ON DELETE CASCADE
    );
"""


with DAG("Workflow_PipeLine_Orchestration_v7",
        default_args=default_args,
        schedule="0 * * * *",
        catchup=False) as dag:
    
    task1 = PythonOperator(
        task_id = "Scrape_HomePage",
        python_callable = Scrape_HomePage
    )
    
    task2 = PythonOperator(
        task_id = "Scrape_TopStories",
        python_callable = Scrape_topstories
    )
    
    task3 = PythonOperator(
        task_id = "Extract_TopStories",
        python_callable = Extract_HeadlineThumbnail
    )
    
    task4 = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_db",  # Connection ID for the Postgres database
        sql=create_tables
    )
    
    task5 = PythonOperator(
        task_id = "Add_Data_to_Tables",
        python_callable = Add_Data_to_DataBase,
        max_active_tis_per_dag=1
    )
        
    task6 = PythonOperator(
        task_id="create_file_task",
        python_callable=Create_Status_File,
        provide_context=True,
    )
    
    file_sensing_task = FileSensor(
    task_id="wait_status_file",
    fs_conn_id="fs_default",
    filepath="{{ ti.xcom_pull(task_ids='create_file_task', key='file_path') }}",
    poke_interval=30,  # Check every 30 seconds
    timeout=600,  # Stop checking after 10 minutes
    mode="poke"
    )
    
    sendEmail_dag = TriggerDagRunOperator(
    task_id="trigger_sendEmail_dag",
    trigger_dag_id="send_email_dag",
    )
    
    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> file_sensing_task >> sendEmail_dag
    

