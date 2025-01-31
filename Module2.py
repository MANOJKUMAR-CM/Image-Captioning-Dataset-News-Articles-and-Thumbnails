import requests 
from bs4 import BeautifulSoup


def Scrape_TopStories(s,config_file = "config.txt"):
    #s = Scrape_HomePage(config_file)

    with open(config_file, 'r') as file:
        urls = [url.strip() for url in file]

    # Reading from the config file.
    heading = urls[1]
    print(heading)
    print()

    # Scraping the Top Stories Link from the Home Page of Google News.

    # To find all <a> tags on the page. 
    Links = s.find_all("a") 
    # It was found on inspecting the Google news WebPage that the Top stories link is in one of the <a> tags.

    topStory_Link = None
    
    #Iterating through all the links and finding if the text in <a> tag matches Top stories read from config file.
    for link in Links:
        if(link.get_text() == heading):
            topStory_Link = link.get('href')
            break
        
    if topStory_Link:
        topStory_Link = "https://news.google.com"+topStory_Link[1:]
        
    print("Top Stories URL: ", topStory_Link)
    print()

    #Sending the request
    topStories_req = requests.get(topStory_Link)

    # Checking the response
    if topStories_req.status_code == 200:
        print("Response of the Server for 'get' request to Top Stories URL: Request Successfull.")
        print()
    else:
        print(f"Failed to retrieve the page. Status code: {topStories_req.status_code}")
        exit()


    S = BeautifulSoup(topStories_req.content, 'html.parser')

    return S


# In Module 2, the Server responds with the HTML content(WebPage @ topStory_Link) which is retrieved using the requests library.
# Using BeautifulSoup, the HTML content is parsed to extract specific elements, such as headlines, links, or any other relevant information.
# By directly fetching the page’s source code, it helps avoid issues related to lazy loading, where certain elements might only appear after JavaScript execution.
# requests retrieves the initial HTML content, the structured data can be accessed immediately without waiting for dynamic content to load asynchronously.