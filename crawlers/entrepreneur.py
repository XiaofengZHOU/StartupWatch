from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse

import unidecode

class CrawlerEntrepreneur:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.name = "Entrepreneur"
        self.articles = []
        self.silent = silent
        base_url = "http://www.entrepreneur.com/topic/technology/"
        self.relative_url_origin = "http://www.entrepreneur.com"
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

                blocks = soup.select(".sectionframe .pl-floathero")  # article_selector
                for block in blocks:
                    link = block.select_one(".block h3 a")["href"]  # url
                    links.append(self.relative_url_origin + link)

                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.extract()  

                    content = ""
                    paragraphs = soup.select(".arttext .bodycopy p")# container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            if "Related:" not in paragraph.getText():
                                content = content + paragraph.getText() + ' '
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        header = soup.select_one(".arttext")
                        date = header.find(itemprop="articlebody")
                        date = date.select_one("time")
                        date = date["datetime"]
                        date = int(parse(date).timestamp())
                    except :
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
                        "origin": "entrepreneur"
                    }

                    if len(content) > 1000:
                        self.articles.append(article)
            except TypeError as e:
                print("Impossible de crawler Entrepreneur : Erreur "+str(e))
                return
            self.log("Entrepreneur crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
