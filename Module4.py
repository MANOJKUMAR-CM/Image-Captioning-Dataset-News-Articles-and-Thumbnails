import psycopg2
import requests
import sys
import io

from io import BytesIO
# Set the standard output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Database connection details
DB_NAME = "News"
DB_USER = "postgres"
DB_PASSWORD = "manu1609"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_tables():
    
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = connection.cursor()

    # Creating images table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id SERIAL PRIMARY KEY,
            image_data BYTEA NOT NULL
        );
    """)

    # Creating headlines table with only image_id and headline
    cur.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            headline_id SERIAL PRIMARY KEY,
            headline TEXT UNIQUE NOT NULL,
            image_id INTEGER REFERENCES images(image_id) ON DELETE CASCADE
        );
    """)

    connection.commit()
    cur.close()
    connection.close()
    
    print("Tables created successfully.")
    print("One Table for the Image data and the other for the corresponding Headline.")
    print()
    
def Insert_image(image_url):
    
    r = requests.get(image_url)
    if r.status_code != 200:
        print(f"Failed to download image: {image_url}")
        return None
    
    img_data = BytesIO(r.content)  
    
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
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
    
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = connection.cursor()
    cur.execute("INSERT INTO headlines (headline, image_id) VALUES (%s, %s);", 
                    (headline, image_id))
    connection.commit()
    print(f"Inserted headline: {headline}")
    
    cur.close()
    connection.close()
