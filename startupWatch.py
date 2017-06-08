from RunCrawlers import *
from ArticlesManager import *
from CompaniesManager import *

num_pages_by_sites = {"TechCrunch":5, "Entrepreneur":5, 
                      "EUStartups":5, "Geekwire":3,
                      "Mashable":5, "RobotReport":1,
                      "TechInsider":5, "TechCo":5,
                      "Venturebeat":5, "StartupDaily":5,
                      "StartupsUK":3, "TechWorld":5,
                      "VentureBurn":5, "StartupBeat":5}
val_page = 3

if __name__ == "__main__":
    '''
    for key, value in num_pages_by_sites.items():
         num_pages_by_sites[key] = value * val_page
    '''

    #crawlers = RunCrawlers()
    #crawlers.runCrawlers()
    #article_manager = ArticlesManager()
    #article_manager.extend_with_watson()
    company_manager = CompaniesManager()
    company_manager.extract_companies()
    company_manager.extend_crunch()
