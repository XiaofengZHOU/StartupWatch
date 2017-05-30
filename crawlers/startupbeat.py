# coding: utf-8

from bs4 import BeautifulSoup
from crawlers.tools import get_html_doc
from dateutil.parser import parse
import time
import json
import re
import unidecode

class CrawlerStartupBeat:
    def __init__(self, number_of_pages_to_crawl):

        self.articles = []
        self.pages = []
        self.name ="StartupBeat"
        base_url = "http://startupbeat.com/page/"
        for x in range(1, number_of_pages_to_crawl + 1):
            self.pages.append(base_url + str(x))
        
        
    def crawl(self):
        pages_length = len(self.pages)
        for idx, page in enumerate(self.pages):
            links = []
            html_doc = get_html_doc(page)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blocks = soup.select("div#masonry article h3 a")
            for block in blocks:
                links.append(block["href"])
             
            #get aarticle of link     
            for link in links:
                html_doc = get_html_doc(link)
                soup = BeautifulSoup(html_doc, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract() 
                content = ""
                paragraphs = soup.select(".post-content p")
                pattern = re.compile(r'\W')
                
                lable = False
                category = soup.select_one("div.post-date-by div.post-categories a").getText()
                if 'startup' in category.lower():
                    lable = True
                    content = content+category.lower()+'. '
                
                for index,para in enumerate(paragraphs):
                    text = para.getText()
                    if len(text)==0:
                        continue   
                    last_letter = text[-1]
                    
                    if lable== True:
                        if index <=2:
                            if pattern.match(last_letter) and last_letter!=' ':
                                content = content+text+' '
                            else:
                                content = content+text+'. '
                                
                        if index >=3:
                            if pattern.match(last_letter) and last_letter!='/':
                                content = content+text+' '
                                
                    if lable == False:
                        if pattern.match(last_letter) and last_letter!='/' :
                                content = content+text+' '
                        
                content = unidecode.unidecode(content)
                content = content.replace(':',' :')
                title = soup.find("h1").getText()
                title = unidecode.unidecode(title)
                date  = soup.find("meta", property="article:published_time")["content"]
                date  = int(parse(date).timestamp()) 

                article = {
                        "title":title,
                        "content":content,
                        "date":date,
                        "url":link,
                        "origin":self.name
                        }
                self.articles.append(article)
            print("StartupBeat crawling at " + str(((idx + 1) / pages_length) * 100) + "%")
    
    def get_articles(self):
        return self.articles
                
                



