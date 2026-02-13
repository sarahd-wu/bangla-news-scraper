import scrapy
from datetime import datetime
import re

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["thedailystar.net"]
    start_urls = ["https://www.thedailystar.net/"]
    # start_urls = ["https://www.thedailystar.net/news/bangladesh/news/teachers-association-expels-former-jamaat-leader-over-ducsu-remark-4092451"]

    def parse(self, response):
        # Collect article links from homepage
        links = response.css('a::attr(href)').getall()

        for link in links:
            if link.startswith("/"):
                link = response.urljoin(link)

            # Filter obvious article URLs
            if "/news/" in link or "/opinion/" in link:
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css("h1::text").get()
        date_text = self.find_article_date(response)          
        if not title or not date_text:
            return

        # Example format: "Tue Jan 28, 2026"
        today = datetime.today().strftime("%Y-%m-%d")
        if today == date_text:
            yield {
                "title": title.strip(),
                "date": date_text.strip(),
                "url": response.url
            }


    def find_article_date(self, response):
        # Finding the date published
        script_texts = response.xpath("//script/text()").getall()
        created = None
        date_text = None
        for text in script_texts:
            if "created" in text and "NodeID" in text:
                match = re.search(r'"created"\s*:\s*"([^"]+)"', text)
                if match:
                    created = match.group(1)
                    clean = created.replace("\\/", "/")
                    date_text = datetime.strptime(
                        clean,
                        "%a, %m/%d/%Y - %H:%M"
                    ).date()
                    date_text = str(date_text)
                    break
                
        return date_text
