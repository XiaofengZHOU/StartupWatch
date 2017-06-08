import time
import json
import os
from util import *

class CompaniesManager:
    def __init__(self):
        init_firefox()
        self.companies = []
        self.articles = []
        self.companies_name = []
        self.load_articles()
        self.load_companies()
        
    def load_articles(self):
        if os.path.isfile('data/raw_articles.json'):
            f = open('data/raw_articles.json')
            self.articles = json.load(f)
            f.close()
            
    def load_companies(self):
        if os.path.isfile('data/raw_companies.json'):
            f = open('data/raw_companies.json')
            self.companies = json.load(f)
            f.close()      
            for company in self.companies:
                name = company["name"]
                self.companies_name.append(name)
        
            
    def extract_companies(self):
        
        for index,article in enumerate(self.articles):
            for company_name in article["companies"]: 
                article_extraInfos = article["extra_infos"]
                for info in article_extraInfos:
                    if info["text"]== company_name:
                        relevance = info["relevance"]
                        count_in_article = info["count"]
                            
                if company_name in self.companies_name :
                    for company in self.companies:
                        if company_name == company["name"] and article["id"] not in company["articles"]: 
                            company["count"] = company["count"]+1
                            company["sentiment"]= company["sentiment"]+article["sentiment"]
                            company["articles"].append(article["id"])
                            extra_infos = {
                                 "id":article["id"] ,
                                 "count_in_article":count_in_article,
                                 "revelance": relevance       
                            }
                            company["extra_infos"].append(extra_infos)
                            
                else:
                    company = {
                        "name": company_name,
                        "dateFound": int(str(time.time()).split('.')[0]),
                        "count":1,
                        "sentiment": article["sentiment"],
                        "articles": [article["id"]],
                        "extra_infos":
                        [
                            {
                             "id": article["id"],
                             "count_in_article":count_in_article,
                             "revelance": relevance
                            }  
                        ]    
                    }
                    self.companies.append(company)
                    self.companies_name.append(company_name)
            
        self.save_to_disk()
        
    def extend_crunch(self):
        
        #for test
        '''
        for index,company in enumerate(self.companies[10:20]):
            name = company["name"]
            search_label = None
            if "search_label" in company:
                search_label = company["search_label"]
                
            if search_label==None :
                url_crunchbase = util.existence_in_crunchbase(name)
                
                if url_crunchbase != None:
                    print(name, ' in crunchbase')
                    founded,employees,website = util.extract_company_techcrunch(name,url_crunchbase)
                    print("founded: ", founded)
                    print("employees: ", employees)
                    print("website: ", website)
                    
                else:
                    company["search_label"] = str(0)
                    print(name, 'not in crunchbase')
            else:
                url_crunchbase = util.existence_in_crunchbase(name)
                print("company has been searched : ")
                print(name, ' in crunchbase')
                founded,employees,website= util.extract_company_techcrunch(name,url_crunchbase)
                print("founded: ", founded)
                print("employees: ", employees)
                print("website: ", website)
            
        '''
        i = 0
        for index,company in enumerate(self.companies):
            name = company["name"]
            search_label = None
            if "search_label" in company:
                search_label = company["search_label"]

            '''  
            # used for update website of the companies already searched 
            if search_label==None or "website" not in company:
                if search_label != None and search_label != str(0):
                    url_crunchbase = company["search_label"]
                elif search_label == str(0):
                    print("skip not found: ", name)
                    continue
                else:
                    url_crunchbase = existence_in_crunchbase(name)
            '''
            
            if search_label == None:
                url_crunchbase = existence_in_crunchbase(name)                  
                if url_crunchbase != None:
                    print(name, ' in crunchbase')
                    i=i+1
                    founded,employees,website = extract_company_techcrunch(name,url_crunchbase)
                    company["search_label"] = url_crunchbase
                    if founded is not None:
                        company["foundationDate"] = founded
                    if employees is not None:
                        company["number_of_employees"] = employees
                    if website is not None:
                        company["website"] = website
                    print(founded, employees, website)
                else:
                    company["search_label"] = str(0)
                    print(name, 'not in crunchbase')
            else:
                print("skip already searched: ", name)
            
            if (i+1)%20 == 0:
                self.save_to_disk()
        self.save_to_disk() 

                                
    def save_to_disk(self):
        with open('data/raw_companies.json', 'w') as company_file:
            json.dump(self.companies, company_file,indent = 2)
            company_file.close()
						