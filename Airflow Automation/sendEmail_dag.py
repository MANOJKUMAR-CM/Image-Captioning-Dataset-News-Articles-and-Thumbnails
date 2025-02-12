from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base import BaseHook
from airflow.operators.email import EmailOperator
from airflow.utils.trigger_rule import TriggerRule
import os
import json


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

def read_file(ti):
    conn = BaseHook.get_connection("fs_default")
    extra = conn.extra or "{}"
    file_path = json.loads(extra).get("path", "/opt/airflow/dags/run/").strip('"')

    full_path = os.path.join(file_path, "status.txt")

    with open(full_path, "r") as f:
        content = f.read().strip()

    print(f"Read from file: {content}")
    ti.xcom_push(key="status_content", value=content)
    ti.xcom_push(key="file_path", value=full_path) 

def check_stories(ti):
    n = ti.xcom_pull(task_ids="read_status_file", key="status_content")
    s = int(n)
    if s > 0:
        return "sendEmail"
    else:
        return "noEmail"
    
def delete_status_file(ti):
    path = ti.xcom_pull(task_ids="read_status_file", key="file_path")
    os.remove(path)
    print("Status file Deleted Successfully.")

with DAG(
    "send_email_dag",
    default_args=default_args,
    schedule=None,  # Triggered by First DAG
    catchup=False
) as dag:

    read_task = PythonOperator(
        task_id="read_status_file",
        python_callable=read_file
    )

    check_stories_task = BranchPythonOperator(
        task_id = "c_stories",
        python_callable = check_stories
    )
    
    send_email = EmailOperator(
        task_id = "sendEmail",
        to = "xyz@smail.iitm.ac.in", # Replace with any gmail I'd
        subject="AIRFLOW: New Records Inserted in Database",
        html_content="""<h3>{{ ti.xcom_pull(task_ids='read_status_file', key='status_content') }} new records inserted.</h3>""",   
    )
    
    no_email = PythonOperator(
        task_id="noEmail",
        python_callable=lambda: print("No new TopStories, i.e, All Duplicates. Skipping Email")
    )
    
    delete_file = PythonOperator(
        task_id="delete_status_file",
        python_callable=delete_status_file,
        trigger_rule=TriggerRule.ALL_DONE  # Executes after when Email sending functionality completes
    )
    
    read_task >> check_stories_task 
    check_stories_task >> send_email
    check_stories_task >> no_email
    [send_email, no_email] >> delete_file

"""
Add this to airflow-webserver and airflow-scheduler in docker-compose.yaml file
environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
      - AIRFLOW__SMTP__SMTP_STARTTLS=True
      - AIRFLOW__SMTP__SMTP_SSL=False
      - AIRFLOW__SMTP__SMTP_USER=********@smail.iitm.ac.in # Replace with user mail i'd
      - AIRFLOW__SMTP__SMTP_PASSWORD=*************** # Add the 16 digit app password from gmail
      - AIRFLOW__SMTP__SMTP_PORT=587
"""