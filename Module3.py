
# On Inspecting the Top stories WebPage, it was observed that the images and the corresponding headlines are clubbed within <article> tag.

def Extract_HeadLine_Thumbnail(S):

    # To find all <article> tags on the page. 
    articles = S.find_all("article")

    Images = []
    Headlines = []

    # Iterating over each article tag
    for article in articles:
        images = article.find("img")
        img_url = images["src"] if images else "No image"
        
        if(img_url[:5] == '/api/'):
            Images.append("https://news.google.com"+img_url)
            
            headline = article.find_all("a")
            Headlines.append(headline[1].get_text())

    Data = [] # (Image_URL, Headline) -> tuples
    for i in range(len(Images)):
        Data.append((Images[i], Headlines[i]))

    print("Thumbnails and the Headlines are extracted!")
    
    return Data
