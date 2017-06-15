from bs4 import BeautifulSoup
from dateutil.parser import parse
#from crawlers.tools import *
from tools import *


import unidecode
import json


class CrawlerStartupDaily:
    def __init__(self, number_of_pages_to_crawl, silent=False):
        self.pages = []
        self.articles = []
        self.name = "StartupDaily"
        self.silent = silent
        self.base_url = "http://www.startupdaily.net/page/"
        self.relative_url_origin = "http://www.startupdaily.net"

        '''
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
        '''
            
        # test change code here
        self.current_page_number = 1
        self.crawl_or_not = True
        self.timestamp = get_timestamp('StartupDaily')


    def set_page(self):
        self.current_page_url = self.base_url + str(self.current_page_number)
        self.current_page_number += 1

        
            
    def crawl(self):
        '''
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
        '''
        temp_timestamp = self.timestamp
        while self.crawl_or_not:
            self.set_page()
            links = []
            try:
                html_doc = get_html_doc(self.current_page_url)
                soup = BeautifulSoup(html_doc, 'html.parser')           
                blocks = soup.select("h2.post-title a")  # article_selector
            except:
                continue
            
            for block in blocks:
                try:
                    link = block["href"]
                    if "http://www.startupdaily.net" in link:
                        links.append(link)
                except:
                    continue

                
            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract() 
                content = ""
                paragraphs = soup.select("div#dslc-theme-content-inner p") # container-selector + text_selector

                for paragraph in paragraphs:
                    if not (paragraph.has_attr('style')):
                        try:
                            content = content + paragraph.getText()+ ' '
                        except:
                            pass
                content = unidecode.unidecode(content)
                
                try:
                    header = soup.find("meta",property="article:published_time")["content"]
                    date = int(parse(header).timestamp())
                except TypeError: 
                    date = soup.select("li.post-date a")[0].getText()
                    date = int(parse(date).timestamp())

                if int(date) <= int(self.timestamp):
                    set_timestamp('StartupDaily', temp_timestamp)
                    self.crawl_or_not = False                    
                    break
                elif int(date) > int(temp_timestamp):
                    temp_timestamp = date
                    print("new article at:", temp_timestamp)
              
                try:
                    title = soup.select_one('head title')
                    title = title.text.split(' - ')[0]
                    title = unidecode.unidecode(title)
                except:
                    continue
                    
                article = {
                    "title": title,
                    "content": content,
                    "date": date,
                    "url": link,
                    "origin": "Startup Daily"
                }

                self.articles.append(article)

        #self.log("Startup Daily Crawling at " + str(((idx + 1) / pages_length) * 100) + "%")

    def get_articles(self):
        return self.articles

    def log(self, message):
        if not self.silent:
            print(message)

