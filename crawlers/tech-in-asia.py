from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

# To run this class we need to install firefox 
class CrawlerTechInAsia:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.silent = silent
        self.base_url = "https://www.techinasia.com/category/startups"
        self.relative_url_origin = "https://www.techinasia.com"

        self.number_of_pages_to_crawl = number_of_pages_to_crawl
        self.browser = webdriver.PhantomJS(executable_path='driver/phantomjs.exe')

    def crawl(self):
        links = []
        self.browser.get(self.base_url)
        for i in range(self.number_of_pages_to_crawl):
            time.sleep(0.5)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        page_of_link = BeautifulSoup(self.browser.page_source, "html.parser")
        blocks = page_of_link.select("article div.post-list__left a.post-list__image")
        for block in blocks:
            try:
                link = block["href"]  # url
                links.append(link)
            except:
                continue

        for i,link in enumerate(links):
            try:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
            except:
                continue
            content = ""
            paragraphs = page.select("div.clearfix p")
            for paragraph in paragraphs:
                content += paragraph.getText()

			try:
                date = page.find("meta",  property="article:modified_time")
                date = date["content"]
                date = int(parse(date).timestamp())
            except:
                date = str(0)

            try :
                title = page.select_one("title").getText()
            except:
                continue

            article = {
                "title": title,
                "content": content,
                "date": date,
                "url": link,
                "origin": "techinasia"
            }
            if len(content) <=1000:
                print("content is not enough or something goes wrong of this link : ", link)
            else:
                self.articles.append(article)
        self.browser.quit()

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)

