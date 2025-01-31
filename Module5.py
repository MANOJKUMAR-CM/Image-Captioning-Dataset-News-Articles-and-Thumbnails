import psycopg2

DB_NAME = "News"
DB_USER = "postgres"  
DB_PASSWORD = "manu1609"  
DB_HOST = "localhost"
DB_PORT = "5432"

# To check if the headline is already present in the Database.
# If the headline is unique then only the data(Image, Headline) is added.

def check(headline):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM headlines WHERE headline = %s;", (headline,))
    count = cur.fetchone()[0]
    if(count > 0):
        print("HeadLine already present in DB: ", headline)
    cur.close()
    connection.close()
    return count > 0
