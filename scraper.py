import requests
from bs4 import BeautifulSoup
import time
import json

def fetch_article_content(text):
    container = text.find("div", class_="clearfix")
    paragraphs = container.find_all("p")
    content = "\n".join([p.get_text() for p in paragraphs])
    return content

def fetch_article_title(text):
    title = text.find("h1").string
    return title

# Target URL
url = "https://www.thedailystar.net/news/world"
list = []
link_set = set()

# Get the webpage
response = requests.get(url)
print("original request", response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("a", href=True)
for article in articles:
     link = article['href']
     if link.startswith("/news/world/"):
         link_set.add("https://www.thedailystar.net" + link)
        
print(link_set)
         

for i, link in enumerate(link_set):
    attempts = 0
    max_retries = 5
    while True:
        response_article = requests.get(link)
        soup_article = BeautifulSoup(response_article.text, "html.parser")
        if response_article.status_code == 403 and attempts < max_retries:
            attempts += 1
            print(f"Received 403 for {link}, retrying in 10s ({attempts}/{max_retries})")
            time.sleep(15)
            continue

        content = fetch_article_content(soup_article)
        title = fetch_article_title(soup_article)
        
        object = {
            "id": i,
            "link": link,
            "title": title,
            "content": content
        }

        list.append(object)
        print(object)

        break

file_path = "output.json"

with open(file_path, 'w') as f:
    json.dump(list, f, indent=4)

# print(dict_link)

# URL = "https://www.thedailystar.net/news/world/news/russia-says-its-ready-respond-venezuelas-appeal-help-4029336"
# response = requests.get(URL)
# soup = BeautifulSoup(response.text, "html.parser")
# test = fetch_article_content(soup)
# heading = fetch_article_title(soup)
# print("\n\n", test)
# print("====================================")
# print(heading)