import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://www.thedailystar.net/news/world"

# Get the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
dict_link = {}
articles = soup.find_all("a", href=True)
print(articles)
for a in articles:
    link = a["href"]
    if link.startswith("/news/world/"):
        dict_link[link] = link

print(dict_link)