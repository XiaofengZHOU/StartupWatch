from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse

import unidecode


class CrawlerGeekwire:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "Geekwire"
        base_url = "http://www.geekwire.com/startups/page/"
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

                blocks = soup.select(".teaser-thumb")  # article_selector
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
                    for script in soup(["script", "style"]):
                        script.extract() 

                    content = ""
                    paragraphs = soup.select(".entry-content p")  # container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content = content + paragraph.getText() + ' '
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        header = soup.select_one(".page-header .published")
                        date = header["datetime"]
                        date = int(parse(date).timestamp())
                    except :
                        date = str(0)

                    try:
                        title = soup.select_one("title").getText().split(' - ')[0]
                        title = unidecode.unidecode(title)
                    except:
                        continue


                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        "url": link,
                        "origin": "geekwire"
                    }

                    self.articles.append(article)
            except ValueError as e:
                print("Impossible de crawler Geekwire : Erreur "+str(e))
                return
            self.log("Geekwire crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
