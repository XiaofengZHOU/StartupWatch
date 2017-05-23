from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
import time
import unidecode


class CrawlerVentureBurn:
    def __init__(self, number_of_pages_to_crawl):

        self.articles = []
        self.pages = []
        self.name ="VentureBurn"
        base_url = "http://ventureburn.com/page/"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
        
        
    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            html_doc = get_html_doc(page)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blocks = soup.select("ul.archive-list li div.archive-text h2 a")
            for block in blocks:
                links.append(block["href"])

            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract() 
                paragraphs = soup.select("div#home-main p")
                if len(paragraphs)==0:
                    paragraphs = soup.select("p")                    
                content = ""
                for para in paragraphs:
                    text = para.getText()
                    content = content+text+' '
                    content = unidecode.unidecode(content)
                            
                    
                title = soup.select_one("div.story-headline h1").getText()
                title = unidecode.unidecode(title)
                date  = soup.find("meta",  property="article:published_time")["content"]
                date  = int(parse(date).timestamp()) 

                article = {
                    "title":title,
                    "content":content,
                    "date":date,
                    "url":link,
                    "origin":"VentureBurn"
                }
                self.articles.append(article)
            
            print("VentureBurn crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
            
    def get_articles(self):
        return self.articles