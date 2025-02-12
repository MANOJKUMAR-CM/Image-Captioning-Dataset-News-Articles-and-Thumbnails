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
The project is organized into modules, each handling a specific task in the pipeline. Here’s an overview of the project structure:

- 📜 Module1.py        # Scrapes the homepage for initial URLs
- 📜 Module2.py        # Extracts top stories from the scraped URLs
- 📜 Module3.py        # Extracts headlines and thumbnails
- 📜 Module4.py        # Handles database interactions (tables, insertions)
- 📜 Module5.py        # Checks for duplicate headlines before inserting
- 📜 Module6.py        # Orchestrates all modules, logs execution
- 📜 config.txt        # Configuration file
- 📜 README.md         # Project documentation
- 📜 pipeline.log      # Logs execution details
- 📂 Airflow Automation # Automating all the scripts using Apache Airflow

## 📌 Pipeline Overview
The image below illustrates the workflow of the image captioning dataset pipeline. It starts with web scraping to collect news headlines and thumbnails, followed by database storage, and concludes with logging and automation for smooth execution.

## 📷 Pipeline Diagram: check `pipeline_diagram.png`

## **📈 Logs**
The pipeline execution details, including timestamps and any errors, are logged into pipeline.log for easy tracking and debugging. You can view the log file to check the status of the pipeline execution, or to troubleshoot any issues.

## **⏳ Airflow Automation**
To streamline execution and automate the pipeline, **Apache Airflow** has been used. The **Airflow Automation** folder contains all necessary scripts and DAGs to manage scheduling and execution.

🔹 **Check the `Airflow Automation` folder** for complete details on setting up and running the automation workflow using Apache Airflow.

## 📧 Contact

If you have questions, suggestions, or just want to connect, feel free to reach out!

- **Name**: Manoj Kumar.CM  
- **Email**: [manoj.kumar@dsai.iitm.ac.in]  
- **GitHub Profile**: [Manoj Kumar C M](https://github.com/MANOJKUMAR-CM)

