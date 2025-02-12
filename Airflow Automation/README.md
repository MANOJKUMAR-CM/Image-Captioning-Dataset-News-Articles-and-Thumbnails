# 🚀 Airflow Pipeline: Web Scraping & Database Automation

## 📌 Overview
This Airflow pipeline orchestrates the scraping of top news stories, extracts relevant data, stores it in a PostgreSQL database, and sends email notifications for new entries.

## 🔧 Workflow Breakdown
1. **Scrape HomePage:** Fetches the HTML content of the homepage.
2. **Scrape Top Stories:** Extracts top news articles from the scraped homepage.
3. **Extract Headlines & Thumbnails:** Parses the HTML to retrieve headlines and corresponding images.
4. **Database Storage:** Stores unique headlines and images in PostgreSQL.
5. **Status File Creation:** Writes the number of new stories to a status file.
6. **File Sensor Check:** Waits for the status file to be created.
7. **Email Notification:** Sends an email if new stories are added.
8. **Cleanup:** Deletes the status file post-processing.

## 🏗 DAG Structure
### `Workflow_PipeLine_Orchestration_v7`
- Scrape homepage → Scrape top stories → Extract headlines & thumbnails → Insert into DB → Create status file → File sensor → Trigger email DAG

### `send_email_dag`
- Read status file → Check new stories → Send email (if new) → Delete status file

## 📂 Database Schema
```sql
CREATE TABLE IF NOT EXISTS images (
    image_id SERIAL PRIMARY KEY,
    image_data BYTEA NOT NULL
);

CREATE TABLE IF NOT EXISTS headlines (
    headline_id SERIAL PRIMARY KEY,
    headline TEXT UNIQUE NOT NULL,
    image_id INTEGER REFERENCES images(image_id) ON DELETE CASCADE
);
```

## 📌 Airflow Configuration
Add the following settings to `docker-compose.yaml` for SMTP support:
```yaml
environment:
  - AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
  - AIRFLOW__SMTP__SMTP_STARTTLS=True
  - AIRFLOW__SMTP__SMTP_SSL=False
  - AIRFLOW__SMTP__SMTP_USER=your_email@domain.com
  - AIRFLOW__SMTP__SMTP_PASSWORD=your_app_password
  - AIRFLOW__SMTP__SMTP_PORT=587
```

## 🛠 Troubleshooting
- **Database Connection Issues:** Ensure PostgreSQL is running and Airflow has the correct connection settings.
- **Email Not Sent:** Check SMTP credentials and app password settings.
- **DAG Not Triggering:** Verify DAG dependencies and scheduling.

## 🎯 Future Enhancements
- Implement parallel processing for improved efficiency.
- Add more robust error handling & logging.
- Extend functionality for additional news sources.

## 📧 Contact

If you have questions, suggestions, or just want to connect, feel free to reach out!

- **Name**: Manoj Kumar.CM  
- **Email**: [manoj.kumar@dsai.iitm.ac.in]  
- **GitHub Profile**: [Manoj Kumar C M](https://github.com/MANOJKUMAR-CM)

🚀 **Happy Automating!** 🎉
