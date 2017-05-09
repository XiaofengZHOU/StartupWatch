from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
import time
import unidecode


class CrawlerTechWorld:
    def __init__(self, number_of_pages_to_crawl):

        self.articles = []
        self.pages = []
        self.name ="TechWorld"
        base_url = "http://www.techworld.com/startups/"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
        
        
    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            html_doc = get_html_doc(page)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blocks = soup.select("ul.listing li.media article.bd a")
            for block in blocks:
                links.append(block["href"])

            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
                content = ""
                
                if soup.select_one("main header.slideshowHeader"):
                    group = soup.select_one("div.titleGroup meta")
                    paragraphs = group.find_all("p",recursive=False)

                    for para in paragraphs:
                        text = para.getText()
                        if "Read next:" in text:
                            text=""
                        content = content+text
                                            
                    blocks = soup.select("section.carousel__item-description")
                    for block in blocks:
                        paragraphs = block.select('p')
                        for para in paragraphs:
                            text = para.getText()
                            if "Read next:" in text:
                                text=""
                            content = content+text+' '
                    content = unidecode.unidecode(content)
                            
                elif soup.select_one("section#articleBody"):
                    paragraphs = soup.select("section#articleBody p")
                    for para in paragraphs:
                        text = para.getText()
                        if "Read next:" in text:
                            text=""
                        content = content+text+' '
                    content = unidecode.unidecode(content) 
                    
                title = soup.find("h1",attrs={"itemprop": "headline"}).getText()
                title = unidecode.unidecode(title)
                date  = soup.select_one("time")["datetime"]
                date  = int(parse(date).timestamp()) 

                article = {
                    "title":title,
                    "content":content,
                    "date":date,
                    "url":link,
                    "origin":"TechWorld"
                }
                self.articles.append(article)
            
            print("TechWorld crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
            
    def get_articles(self):
        return self.articles