# Image Captioning Dataset: News Articles and Thumbnails
This project focuses on building a pipeline to extract **news headlines** and their associated **thumbnails** from a news website. The extracted images and headlines are saved in a **PostgreSQL database**, and the entire process is logged for debugging and automation purposes. The dataset can be used for tasks like **image captioning** and **text-image associations**.

---

## **📌 Features**  

- **Web Scraping**: Extracts **news headlines** and **thumbnails** from a website.  
- **Database Storage**: Saves extracted data (headlines & images) in a **PostgreSQL database**.  
- **Logging**: Tracks the execution of the pipeline with detailed logs for debugging.  
- **Automation**: Easily configurable to run on a schedule using **CronJob**.  
- **Data for Image Captioning**: This pipeline creates a dataset with news article headlines and their corresponding image thumbnails, perfect for **image captioning** tasks.

## **📂 Project Structure**
- 📜 Module1.py        # Scrapes the homepage for initial URLs
- 📜 Module2.py        # Extracts top stories from the scraped URLs
- 📜 Module3.py        # Extracts headlines and thumbnails
- 📜 Module4.py        # Handles database interactions (tables, insertions)
- 📜 Module5.py        # Checks for duplicate headlines before inserting
- 📜 Module6.py        # Orchestrates all modules, logs execution
- 📜 config.txt        # configuration file
- 📜 README.md         # Project documentation
- 📜 pipeline.log      # Logs execution details
