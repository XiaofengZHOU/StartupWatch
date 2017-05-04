from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
import time
import unidecode
from dateutil.parser import parse

class CrawlerTechcrunch:
    def __init__(self, number_of_pages_to_crawl, silent = False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name ="Techcrunch"
        base_url = "http://techcrunch.com/startups/page/"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
            time.sleep(5)

    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []

            html_doc = get_html_doc(page)
            try:
                soup = BeautifulSoup(html_doc, 'html.parser')

                blocks = soup.select(".river-block")
                for block in blocks:
                    article_type_text = ""
                    article_type = block.select_one(".block .tags .tag span")
                    if article_type is not None:
                        article_type_text = article_type.getText()
                    if article_type_text == "Startups" or article_type_text == "":
                        link = block.select_one(".post-title a")["href"]
                        links.append(link)

                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')

                    content = ""
                    paragraphs = soup.select("div.article-entry p")
                    for paragraph in paragraphs:
                        try:
                            if 'id'  in paragraph.attrs.keys():
                                content = ""
                            content += paragraph.getText()
                        except AttributeError:
                            print("Attribute error !")
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        date = soup.find(attrs={'name':'timestamp'})['content']
                        date = int(parse(date).timestamp())
                    except TypeError:
                        date = str(0)

                    tags = []
                    tags_container = soup.select(".article-header .tags .tag-item .tag")
                    for tag in tags_container:
                        tags.append(tag.getText())

                    article = {
                        "title": unidecode.unidecode(soup.select_one("h1.tweet-title").getText()),
                        "content": content,
                        "date": date,
                        "tags": tags,
                        "url": link,
                        "origin": "techcrunch"
                    }

                    self.articles.append(article)
                self.log("Techcrunch crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
            except TypeError as e:
                print("Article fetching failed")



    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
