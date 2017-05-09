from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
import time
import unidecode

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class CrawlerMashable:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.driver = webdriver.PhantomJS(executable_path='driver/phantomjs.exe')
        self.articles = []
        self.name ="Mashable"
        self.silent = silent
        base_url = "http://mashable.com/category/startups/"

        self.driver.get(base_url)
        for i in range(number_of_pages_to_crawl):
            time.sleep(0.5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def crawl(self):
        links = []
        soup  = BeautifulSoup(self.driver.page_source, "html.parser")
        blocks = soup.select(".article-content-wrapper") #article_selector
        for block in blocks:
            try:
                link = block.select_one(".article-content .article-title a")["href"]# url
                links.append(link)
            except:
                continue

               
        for link in links:
            try:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
            except:
                continue

            content = ""
            paragraphs = soup.select(".article-content p")# container-selector + text_selector
            for paragraph in paragraphs:
                try:
                    content = content + paragraph.getText()+ ' '
                except AttributeError:
                    print("AttributeError in getting text")
                    pass
            content = unidecode.unidecode(content)

            try:
                header = soup.select_one(".article-info time")
                if header is not None:
                    date = header["datetime"]
                    date = int(parse(date).timestamp())
                else:
                    date = str(0)
            except ValueError:# TypeError
                date = str(0)

            try:
                title = soup.select_one(".article-header .title").getText()
                title = unidecode.unidecode(title)
            except :
                title =""
                continue

            article = {
                "title": title,
                "content": content,
                "date": date,
                "url": link,
                "origin": "mashable"
            }
            self.articles.append(article)

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)
