import logging
import sys
import time

from Module1 import Scrape_HomePage
from Module2 import Scrape_TopStories
from Module3 import Extract_HeadLine_Thumbnail
from Module4 import create_tables, Insert_image, Insert_headline
from Module5 import check

log_file = "pipeline.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_event(message, level = 'info'):
    if level == "info":
        logging.info(message)
    elif level == "Error":
        logging.error(message)
    print(message)
    

def AddData_to_DB(data):
    for image_path, headline in data:
        if not check(headline):
                image_id = Insert_image(image_path)
                Insert_headline(headline, image_id)

def PipeLine():
    start = time.time()
    log_event("PipeLine Execution Started!")
    try:
        log_event("Executing Module 1")
        s = Scrape_HomePage()
        log_event("Completed Executing Module 1")
        
        log_event("Executing Module 2")
        S = Scrape_TopStories(s)
        log_event("Completed Executing Module 2")
        
        log_event("Executing Module 3")
        Data = Extract_HeadLine_Thumbnail(S)
        log_event("Completed Executing Module 3")
        
        log_event("Executing Module 4")
        create_tables()
        log_event("Completed Executing Module 4")
        
        log_event("Executing Module 5")
        AddData_to_DB(Data)
        log_event("Completed Executing Module 5")
        
        
    except Exception as e:
        log_event(f"Pipeline execution failed: {str(e)}", level="error")
        sys.exit(1)
        
    end = time.time()
    log_event(f"Pipeline execution completed in {end - start:.2f} seconds.")
    
if __name__ == "__main__":
    PipeLine()