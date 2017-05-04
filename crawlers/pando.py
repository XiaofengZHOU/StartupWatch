from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse


class CrawlerPando:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "Pando"
        base_url = "http://pando.com/archives/?page="
        self.relative_url_origin = "http://pando.com/"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))

    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            html_doc = get_html_doc(page)

            soup = BeautifulSoup(html_doc, 'html.parser')

            blocks = soup.select(".wrapper")  # article_selector
            for block in blocks:
                # article_type_text = ""
                # article_type = block.select_one(".block .tags .tag span")
                # if article_type is not None:
                #     article_type_text = article_type.getText()
                # if article_type_text == "Startups" or article_type_text == "":

                link = block.select_one(".extract h2 a")["href"]  # url
                links.append(self.relative_url_origin + link)

            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')

                content = ""
                paragraphs = soup.select(".contains-copy p")# container-selector + text_selector
                for paragraph in paragraphs:
                    try:
                        content += paragraph.getText()
                    except AttributeError:
                        print("AttributeError in getting text")
                        pass
                try:
                    header = soup.select_one("#byline span")
                    if header is not None:
                        date = header.contents[-1]
                        date = int(parse(date).timestamp())
                    else:
                        date = str(0)
                except AttributeError:  # TypeError
                    date = str(0)

                # tags = []
                # tags_container = soup.select(".article-header .tags .tag-item .tag") #tag; optionnel
                # for tag in tags_container:
                #     tags.append(tag.getText())

                title = soup.select_one("#content #intro .shim h1")
                if title is not None:
                    title = title.text
                else:
                    title = ""

                article = {
                    "title": title,
                    "content": content,
                    "date": date,
                    # "tags": tags,
                    "url": link,
                    "origin": "pando"
                }

                self.articles.append(article)

            self.log("Pando crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
