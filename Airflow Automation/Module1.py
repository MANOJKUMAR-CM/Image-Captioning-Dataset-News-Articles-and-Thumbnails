import requests 
from bs4 import BeautifulSoup
import os
# To Scrape the Home Page of Google News
# URL is configured by a config file

config_file = os.path.join(os.path.dirname(__file__), "config.txt")

def Scrape_HomePage(config_file = config_file):
    # Reading the WebPage from a config file
    with open(config_file, 'r') as file:
        urls = [url.strip() for url in file]

    url = urls[0]
    print("WebPage URL:", url)
    print()

    # Scraping the WebPage
    
    # Sending the request
    req = requests.get(url) 

    # Checking the response
    if req.status_code == 200:
        print("Response of the Server for 'get' request to HomePage(Google News) URL:Request Successfull.")
        print()
    else:
        print(f"Failed to retrieve the page. Status code: {req.status_code}")
        exit()

    # Parsing the response to navigate to find the desired element
    s = BeautifulSoup(req.content, 'html.parser')

    return str(s)
