import json
import os 
import re

from crawlers.entrepreneur import CrawlerEntrepreneur
from crawlers.eustartups import CrawlerEUStartups
from crawlers.geekwire import CrawlerGeekwire
from crawlers.mashable import CrawlerMashable
from crawlers.robot_report import CrawlerRobotReport
from crawlers.startupbeat import CrawlerStartupBeat
from crawlers.startupdaily import CrawlerStartupDaily
from crawlers.startupuk import CrawlerStartupsUK
from crawlers.tech_co import CrawlerTechCo
from crawlers.tech_insider import CrawlerTechInsider
from crawlers.techcrunch import CrawlerTechcrunch
from crawlers.techworld import CrawlerTechWorld
from crawlers.venturebeat import CrawlerVenturebeat
from crawlers.ventureburn import CrawlerVentureBurn


class RunCrawlers:
    def __init__(self, num_pages_by_sites):
        self.articles = {}
        self.path_database = "data/data.json"
        self.crawlers = []
        self.keys = ["Techcrunch","Entrepreneur","EUStartups","Geekwire","Mashable","RobotReport","TechInsider",
                     "TechCo","Venturebeat","StartupDaily","StartupsUK","TechWorld","VentureBurn","StartupBeat"]
        
        self.setArticles()
        self.setCrawlers(num_pages_by_sites)
        
        
    def setArticles(self): 
        """
        case1: database file exists 
        """
        
        """
        case2: database file does not exist
        """
        if os.path.isfile(self.path_database): 
            with open(self.path_database,'r') as f:
                self.articles = json.load(f)    
                f.close()
                for key in self.keys:
                    if key not in self.articles.keys():
                        self.articles[key] = []

        else:
            for key in self.keys:
                self.articles[key] = []
                
    """
    Using this function, we can choose the crawlers and the number of pages of every crawler.
    Example:
    num_pages_by_sites ={"TechCrunch":5, "Geekwire":3}
    self.setCrawlers(num_pages_by_sites)
    """    
    def setCrawlers(self,num_pages_by_sites):
        for key in num_pages_by_sites.keys():
            if key == "RobotReport":
                self.crawlers.append( CrawlerRobotReport(num_pages_by_sites["RobotReport"]) )
            if key == "Techcrunch":
                self.crawlers.append( CrawlerTechcrunch(num_pages_by_sites["Techcrunch"]) )
            if key == "Mashable":
                self.crawlers.append( CrawlerMashable(num_pages_by_sites["Mashable"]) )
            if key == "Entrepreneur":
                self.crawlers.append( CrawlerEntrepreneur(num_pages_by_sites["Entrepreneur"]) )
            if key == "TechInsider":
                self.crawlers.append( CrawlerTechInsider(num_pages_by_sites["TechInsider"]) )
            if key == "Geekwire":
                self.crawlers.append( CrawlerGeekwire(num_pages_by_sites["Geekwire"]) )
            if key == "TechCo":
                self.crawlers.append( CrawlerTechCo(num_pages_by_sites["TechCo"]) )
            if key == "Venturebeat":
                self.crawlers.append( CrawlerVenturebeat(num_pages_by_sites["Venturebeat"]) )
            if key == "StartupDaily":
                self.crawlers.append( CrawlerStartupDaily(num_pages_by_sites["StartupDaily"]) )
            if key == "EUStartups":
                self.crawlers.append( CrawlerEUStartups(num_pages_by_sites["EUStartups"]) )
            if key == "StartupsUK":
                self.crawlers.append( CrawlerStartupsUK(num_pages_by_sites["StartupsUK"]) )
            if key == "TechWorld":
                self.crawlers.append( CrawlerTechWorld(num_pages_by_sites["TechWorld"]) )
            if key == "VentureBurn":
                self.crawlers.append(CrawlerVentureBurn(num_pages_by_sites["VentureBurn"]) )
            if key == "StartupBeat":
                self.crawlers.append(CrawlerStartupBeat(num_pages_by_sites["StartupBeat"]) )
                
                
    
    """
    Run the crawlers
    """            
    def runCrawlers(self):
        articles_total = 0
        for crawler in self.crawlers:
            crawler.crawl()
            articles = crawler.get_articles()
            
            print("*********************************************************")
            filtered_articles = self.filter_startup(articles)   
            print("number of articles crawled about startups : ", len(filtered_articles) )
            filtered_articles = self.filter_by_database(filtered_articles,crawler.name)     
            print("number of articles crawled to add in the database : ", len(filtered_articles) )
            self.articles[crawler.name] = filtered_articles + self.articles[crawler.name]           
            articles_total = articles_total+len(filtered_articles)
            print("number of articles of this site in the database before remove repetition : ", len(self.articles[crawler.name] ) )
            
            articles_without_repetition =[]
            for index,article in enumerate(self.articles[crawler.name]):
                if article not in self.articles[crawler.name][index+1:]:
                    articles_without_repetition.append(article)
            self.articles[crawler.name] = articles_without_repetition
            
            print("number of articles of this site in the database after remove repetition : ", len(self.articles[crawler.name] ) )
            print("*********************************************************\n")
            
            self.save_articles()
        
    
    """
    the word startup need to be in content or title.
    """
    def filter_startup(self,articles):
        pattern = re.compile('\W')
        filtered_articles = []
        for article in articles:
            title = re.sub( pattern, '', article["title"].lower() )
            content = re.sub( pattern, '', article["content"].lower())
            if "startup" in title or "startup" in content:
                filtered_articles.append(article)
        return filtered_articles
    
    """
    avoid adding the same article in the database
    """
    def filter_by_database(self,articles,name_crawler):
        pattern = re.compile('\W')
        if name_crawler not in self.articles.keys():
            self.articles[name_crawler] = []            
        articles_database = self.articles[name_crawler]
        if len(articles_database) !=0:
            for article_database in articles_database:
                for article in articles:
                    if re.sub( pattern, '', article["title"].lower() ) == re.sub(pattern,'',article_database["title"].lower()) or article["url"]==article_database["url"]:
                        articles.remove(article)                        
        return articles
        
    
    def save_articles(self):
        with open('data/data.json', 'w') as f:
            json.dump(self.articles, f,indent=2)
            f.close()