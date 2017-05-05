from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
import json
import unidecode

class CrawlerStartupsUK:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.name = "StartupsUK"
        base_url = "http://startups.co.uk/tech-start-up-news/page/"
        self.relative_url_origin = "http://startups.co.uk"
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
                blocks = soup.select("div.article-listing article h2 a") 
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
                    paragraphs = soup.select(".content-main p")# container-selector + text_selector
                    for paragraph in paragraphs:
                        try:
                            content += paragraph.getText()
                        except AttributeError:
                            pass
                    content = unidecode.unidecode(content)
                    try:
                        date = soup.find("meta",  property="article:published_time")
                        if date is not None:
                            date = date["content"]
                            date = int(parse(date).timestamp())
                        else:
                            date = soup.select("div.post-date")[0].getText()
                            date = date.split(':')[-1]
                            date = int(parse(date).timestamp())
                    except TypeError:
                        date = str(0)
                    except AttributeError:
                        date = str(0)                       
                    title = soup.select_one("div.title-block h1").getText()
                    title = unidecode.unidecode(title)
                    article = {
                        "title": title,
                        "content": content,
                        "date": date,
                        "url": link,
                        "origin": "startupuk"
                    }
                    self.articles.append(article)
            except TypeError as e:
                print("Impossible de crawler startupuk: Erreur "+str(e))
                return
            self.log("startup.uk crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
    def get_articles(self):
        return self.articles

    def save_articles(self):
        with open('startupuk.json', 'w') as f:
            json.dump(self.articles, f)

    def log(self, message):
        if not self.silent:
            print(message)


