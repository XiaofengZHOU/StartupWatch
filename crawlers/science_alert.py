from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse



class CrawlerScienceAlert:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "ScienceAlert"
        base_url = "http://www.sciencealert.com/tech/"
        self.relative_url_origin = "http://www.sciencealert.com"
        self.pages.append(base_url)

    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []

            try:
                html_doc = get_html_doc(page)
                soup = BeautifulSoup(html_doc, 'html.parser')

                blocks = soup.select(".article-container-height") #article_selector
                for block in blocks:
                    # article_type_text = ""
                    # article_type = block.select_one(".block .tags .tag span")
                    # if article_type is not None:
                    #     article_type_text = article_type.getText()
                    # if article_type_text == "Startups" or article_type_text == "":

                    link = block.select_one("div.titletext a")["href"]# url
                    links.append(self.relative_url_origin + link)

                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')

                    content = ""
                    paragraphs = soup.select(".main-article .article-fulltext p")# container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content += paragraph.getText()
                        except AttributeError:
                            pass
                    try:
                        header = soup.select_one(".author-name-text")
                        div = header.contents[3]
                        span = div.find("span")
                        date = int(parse(span.text).timestamp())
                    except TypeError:
                        date = str(0)

                    # tags = []
                    # tags_container = soup.select(".article-header .tags .tag-item .tag") #tag; optionnel
                    # for tag in tags_container:
                    #     tags.append(tag.getText())

                    article = {
                        "title": soup.select_one(".article-title").getText(),
                        "content": content,
                        "date": date,
                        # "tags": tags,
                        "url": link,
                        "origin": "scienceAlert"
                    }

                    self.articles.append(article)
            except TypeError as e:
                print("Impossible de crawler Science Alert : Erreur "+str(e.code))
                return
            self.log("ScienceAlert crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
