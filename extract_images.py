import psycopg2
from PIL import Image
import io
import os

# Database credentials
DB_NAME = "News"
DB_USER = "postgres"  
DB_PASSWORD = "manu1609"  
DB_HOST = "localhost"
DB_PORT = "5432"

# Directory to save extracted images
SAVE_DIR = "extracted_images"
os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist

def extract_and_save_images():
    
    
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = connection.cursor()
    
    # Query to fetch image data
    cur.execute("SELECT image_id, image_data FROM images;")
    images = cur.fetchall()

    for image_id, binary_data in images:
        image = Image.open(io.BytesIO(binary_data))  # Convert binary data to an image
        image_path = os.path.join(SAVE_DIR, f"image_{image_id}.png")  # Save as PNG
        image.save(image_path)  # Save the image
        print(f"Image {image_id} saved at {image_path}")

    cur.close()
    connection.close()
    print("All images have been extracted and saved.")

# Run the extraction
extract_and_save_images()


