from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse

import time

import unidecode

class CrawlerTechCo:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "TechCo"
        base_url = "http://tech.co/page/"
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
                blocks = soup.select(".hero-article")  # article_selector
                for block in blocks:
                    aList = block.select('a')
                    for a in aList:
                        if len(a.select('div')) !=0:
                            link = a["href"]
                            links.append(link)


                for link in links:
                    time.sleep(2)
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')

                    content = ""
                    paragraphs = soup.select(".content-wrap .dropcap p")  # container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content = content + paragraph.getText()+ ' '
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        header = soup.select_one(".datetime h2 span")
                        date = header.text
                        date = int(parse(date).timestamp())
                    except TypeError:
                        date = str(0)
                    except AttributeError:
                        date = str(0)

                    try:
                        title = soup.select_one("title").getText()
                        title = unidecode.unidecode(title)
                    except:
                        continue

                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        "url": link,
                        "origin": "tech_co"
                    }

                    self.articles.append(article)
                time.sleep(10)
            except ValueError as e:
                print("Impossible de crawler Tech.co : Erreur "+str(e))
                return
            self.log("Tech.co crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
