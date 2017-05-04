from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
import time
from dateutil.parser import parse

import unidecode


class CrawlerRobotReport:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.name = "RobotReport"
        self.silent = silent
        self.base_url = "https://www.therobotreport.com"
        for x in range(0, number_of_pages_to_crawl):
            self.pages.append(self.base_url + "/news/P" + str(x * 20))

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

                blocks = soup.select("#wrapper > section > section > div > div > h2 a")
                for block in blocks:
                    link = block["href"]
                    links.append(self.base_url + link)

                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')

                    content = ""
                    paragraphs = soup.select("article p")
                    for paragraph in paragraphs[1:]:
                        try:
                            content += paragraph.getText()
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        title = soup.select_one("h1").getText()
                        title = unidecode.unidecode(title)
                    except TypeError:
                        title = str(0)
                    except AttributeError:
                        title = str(0)

                    try:
                        date = paragraphs[0].getText()
                        date = date.split()
                        date = int(parse(date[2]).timestamp())
                    except :
                        date= str(0)

                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        "url": link,
                        "origin": "robot report"
                    }

                    self.articles.append(article)
            except ValueError as e:
                print("Impossible de crawler robot_report : Erreur "+str(e))
                return
            self.log("robot_report crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
