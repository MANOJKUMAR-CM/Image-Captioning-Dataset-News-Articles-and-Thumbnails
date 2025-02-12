from airflow.hooks.postgres_hook import PostgresHook
import requests
from io import BytesIO

def postgres_connection():
    
    postgres_hook = PostgresHook(postgres_conn_id='postgres_db')
    conn = postgres_hook.get_conn()  
    return conn

def Insert_image(image_url):
    r = requests.get(image_url)
    if r.status_code != 200:
        print(f"Failed to download image: {image_url}")
        return None
    
    img_data = BytesIO(r.content)
    
    connection = postgres_connection()
    cur = connection.cursor()
    
    cur.execute("INSERT INTO images (image_data) VALUES (%s) RETURNING image_id;", (img_data.getvalue(),))
    image_id = cur.fetchone()[0]
    
    connection.commit()
    cur.close()
    connection.close()
    
    return image_id

def Insert_headline(headline, image_id):
    # Insert a headline with an associated image.
    if image_id is None:
        print(f"Skipping headline due to missing image: {headline}")
        return
    
    # Get the connection from Airflow
    connection = postgres_connection()
    cur = connection.cursor()
    cur.execute("INSERT INTO headlines (headline, image_id) VALUES (%s, %s);", 
                (headline, image_id))
    connection.commit()
    print(f"Inserted headline: {headline}")
    
    cur.close()
    connection.close()

def check(headline):
    # Check if the headline already exists in the database
    connection = postgres_connection()
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM headlines WHERE headline = %s;", (headline,))
    count = cur.fetchone()[0]
    
    if count > 0:
        print(f"Headline already present in DB: {headline}")
    
    cur.close()
    connection.close()
    
    return count > 0

