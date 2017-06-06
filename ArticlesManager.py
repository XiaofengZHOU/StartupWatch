import json
import uuid
import sys
import os
import copy

from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

#edf6068d-ef4d-4a22-8157-86bb3afb6d2f
#jbtnJKz24PE2

#8cf20702-d26c-40c0-a545-dc5de1ac9862
#vf2l4eYowr5p

#ad5a5ab2-de22-4c51-bb85-8653d2835a5b
#H18pEE8ebBGu

#268eb325-7903-4620-8c95-34523b86daee
#GdToLV3Ar6m5

#8662b280-a060-4b1e-935b-440fca3ae61e
#rl4LIHoomyMq

#ec5dad67-cedb-4cf4-8a7a-9f5fe11e9dd8
#HKYsLJxAAaks

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username="ad5a5ab2-de22-4c51-bb85-8653d2835a5b",
    password="H18pEE8ebBGu")

f1= open('data/name_restrictions.json')
restrictions = json.load(f1)
f1.close()

f2= open('data/name_of_big_companies.json') 
name_not_startup_dic = json.load(f2)
name_not_startup = name_not_startup_dic["names"]
f2.close()

def watson_NLU(url=None,text=None):
    if text == None:
        response = natural_language_understanding.analyze(url=url,features=[features.Entities(),features.Sentiment()],)
    else:
        response = natural_language_understanding.analyze(text=text,features=[features.Entities(),features.Sentiment()],)
        
    entities  = response["entities"]
    sentiment = response["sentiment"]
    return entities,sentiment

def extract_companies(entities):
    companies = []
    names = []
    for entity in entities:
        if entity["type"] == "Company":
            name = entity["text"]
            if filter_company(name):
                companies.append(entity)
                names.append(name)
    return companies,names



def extract_sentiment(sentiment_text):
    score = sentiment_text["document"]["score"]   
    if score >= 0.35:
        sentiment = 1
    elif score <= -0.35:
        sentiment = -1
    else:
        sentiment =0
    return sentiment
        

def filter_company(name):
    label = True
    if name.lower() in name_not_startup:
        label = False
    else:
        for restriction in restrictions:
            if restriction in name.lower():
                label = False
    return label

class ArticlesManager:
    def __init__(self):
        self.articles_by_site = {}
        self.raw_articles = []
        self.raw_articles_new =[]
        self.load_articles()
        
    def load_articles(self):
        if os.path.isfile('data/data.json'):
            f = open('data/data.json')
            self.articles_by_site = json.load(f)
            f.close()
        
        if os.path.isfile('data/raw_articles.json'):
            f1 = open('data/raw_articles.json')
            self.raw_articles = json.load(f1)
            f1.close()
        
    def extend_with_watson(self):
#         urls = []
#         titles=[]
#         for raw_article in self.raw_articles:
#             titles.append(raw_article["title"])
#             urls.append(raw_article["url"])
        articles_by_site = copy.deepcopy(self.articles_by_site)      
        for key in articles_by_site.keys():
            for index,article in enumerate(articles_by_site[key]):
                content = article['content']
                title = article['title']
                url = article['url']
                
                if "id" in article.keys():
                    continue
                    
                else:
                    try:
                        entities,sentiment_dic = watson_NLU(text =content)
                        companies,names  = extract_companies(entities)
                        sentiment = extract_sentiment(sentiment_dic)
                        article["companies"] = names
                        article["extra_infos"] = companies
                        article["sentiment"] = sentiment
                        article["id"] = str(uuid.uuid1())
                        self.raw_articles.append(article)
                        self.raw_articles_new.append(article)
                        self.articles_by_site[key][index]["id"] = article["id"]
                        
                    except KeyboardInterrupt:
                        self.save_to_disk()
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))

                    if len(self.raw_articles)%20 == 0:
                        self.save_to_disk()
        self.save_to_disk()
                
    def save_to_disk(self):
        with open('data/raw_articles.json', 'w') as article_file:
            json.dump(self.raw_articles, article_file,indent = 2)
            article_file.close()
            
        with open('data/raw_articles_new.json', 'w') as article_file:
            json.dump(self.raw_articles_new, article_file,indent = 2)
            article_file.close()
            
        with open('data/data.json', 'w') as article_file:
            json.dump(self.articles_by_site, article_file,indent = 2)
            article_file.close()
            