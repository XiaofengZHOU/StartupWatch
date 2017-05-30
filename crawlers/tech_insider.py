from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
from dateutil.relativedelta import *
import datetime
import calendar
import unidecode 


class CrawlerTechInsider:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "TechInsider"
        base_url = "http://www.techinsider.io/archives?vertical=tech&date="
        self.relative_url_origin = "http://www.techinsider.io"
        current = datetime.date.today()
        minus_one_day = relativedelta(days=-1)

        for i in range(1, number_of_pages_to_crawl):
            self.pages.append(base_url + str(current))
            current += minus_one_day

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

                blocks = soup.select(".river .title-link")  # article_selector
                for block in blocks:
                    # article_type_text = ""
                    # article_type = block.select_one(".block .tags .tag span")
                    # if article_type is not None:
                    #     article_type_text = article_type.getText()
                    # if article_type_text == "Startups" or article_type_text == "":

                    link = block["href"]  # url
                    links.append(self.relative_url_origin + link)

                for link in links:
                    html_doc = get_html_doc(link)
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.extract() 
                    content = ""
                    paragraphs = soup.select(".post-content p")# container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content = content + paragraph.getText()+ ' '
                        except AttributeError:
                            pass
                    content = ' '.join(content.split())
                    content = unidecode.unidecode(content)
                    try:
                        header = soup.select_one(".sl-layout-post .river-post__date span:nth-of-type(2)")
                        date = int(parse(header.text).timestamp())
                    except TypeError:
                        date = str(0)
                    except AttributeError:
                        date = str(0)

                    try:
                        title = soup.select_one("div.sl-layout-post h1").getText()
                        title = unidecode.unidecode(title)
                    except TypeError:
                        title = str(0)
                    except AttributeError:
                        continue
                        title = str(0)
                    # tags = []
                    # tags_container = soup.select(".article-header .tags .tag-item .tag") #tag; optionnel
                    # for tag in tags_container:
                    #     tags.append(tag.getText())
                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        # "tags": tags,
                        "url": link,
                        "origin": "techInsider"
                    }

                    self.articles.append(article)
            except TypeError as e:
                print("Impossible de crawler TechInsider : Erreur "+str(e))
                return
            self.log("TechInsider crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)

