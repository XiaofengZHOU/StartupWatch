from bs4 import BeautifulSoup
from dateutil.parser import parse
from crawlers.tools import get_html_doc


class CrawlerStartupDaily:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.name = "StartupDaily"
        self.silent = silent
        base_url = "http://www.startupdaily.net/page/"
        self.relative_url_origin = "http://www.startupdaily.net"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
            
    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            html_doc = get_html_doc(page)

            soup = BeautifulSoup(html_doc, 'html.parser')
            
            blocks = soup.select("article")  # article_selector
            
            for block in blocks:
                if block.select_one("section div div div ul li a").string=="Startups":
                    link = block.select_one("section div div div h2 a")["href"]  # url
                    links.append(link)
                # article_type_text = ""
                # article_type = block.select_one(".block .tags .tag span")
                # if article_type is not None:
                #     article_type_text = article_type.getText()
                # if article_type_text == "Startups" or article_type_text == "":
              
                
            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
                content = ""
                aux = soup.select("#dslc-theme-content-inner") # container-selector + text_selector
                paragraphs = BeautifulSoup(str(aux[0]),'html.parser')
                paragraphs = paragraphs.find_all('p')
                for paragraph in paragraphs:
                    test = BeautifulSoup(str(paragraph),'html.parser')
                    if not (test.p.has_attr('style')):
                        try:
                            content += paragraph.getText()
                        except AttributeError:
                            print("AttributeError in getting text")
                            pass
                
                try:
                    header = soup.find("meta",property="article:published_time")["content"]
                    
                    if header is not None:
                        date = header.split('T')[0]
                        date = int(parse(date).timestamp())
                    else:
                        date = str(0)
                except AttributeError:  # TypeError
                    date = str(0)

                # tags = []
                # tags_container = soup.select(".article-header .tags .tag-item .tag") #tag; optionnel
                # for tag in tags_container:
                #     tags.append(tag.getText())

                title = soup.select_one('head title')
               
                if title is not None:
                    title = title.text.split('-')[0]
                   
                else:
                    title = ""

                article = {
                    "title": title,
                    "content": content,
                    "date": date,
                    # "tags": tags,
                    "url": link,
                    "origin": "Startup Daily"
                }

                self.articles.append(article)

            self.log("Startup Daily Crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)