from bs4 import BeautifulSoup
from dateutil.parser import parse
from crawlers.tools import get_html_doc
import json

import unidecode

class CrawlerEUStartups:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "EUStartups"
        base_url = "http://www.eu-startups.com/page/"
        self.relative_url_origin = "http://www.eu-startups.com"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
            
    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            try:
                html_doc = get_html_doc(page)
                if html_doc is None:
                    print("Failure in getting HTML doc")
                    return 
                soup = BeautifulSoup(html_doc, 'html.parser')
                blocks = soup.select("div.td-module-image div.td-module-thumb a") 
                for block in blocks:
                    # article_type_text = ""
                    # article_type = block.select_one(".block .tags .tag span")
                    # if article_type is not None:
                    #     article_type_text = article_type.getText()
                    # if article_type_text == "Startups" or article_type_text == "":

                    link = block["href"]  # url
                    links.append(link)
                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    content = ""
                    paragraphs = soup.select("div.td-post-content p")# container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content = content + paragraph.getText() + ' '
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        date = soup.select_one("span.td-post-date time")
                        date = date["datetime"]
                        date = int(parse(date).timestamp())
                    except :
                        date = str(0)

                    try:
                        title = soup.select_one("h1.entry-title").getText()
                        title = unidecode.unidecode(title)
                    except:
                        continue

                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        "url": link,
                        "origin": "eu-startups"
                    }
                    self.articles.append(article)
            except TypeError as e:
                print("Impossible de crawler Entrepreneur : Erreur "+str(e))
                return
            self.log("eu startups crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
    def get_articles(self):
        return self.articles

    def save_articles(self):
        with open('eustartups.json', 'w') as f:
            json.dump(self.articles, f)

    def log(self, message):
        if not self.silent:
            print(message)