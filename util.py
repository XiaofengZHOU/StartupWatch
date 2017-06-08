from bs4 import BeautifulSoup
from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

import sys


def init_firefox():
    global firefox
    global driver
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['handleAlerts'] = True
    firefox_capabilities['acceptSslCerts'] = True
    firefox_capabilities['acceptInsecureCerts'] = True
    geckoPath = 'driver/geckodriver.exe'
    #capabilities=firefox_capabilities,
    firefox = webdriver.Firefox(executable_path=geckoPath)
    #driver = webdriver.PhantomJS(executable_path='driver/phantomjs.exe')
    driver = webdriver.Firefox( executable_path=geckoPath)
    try:
        firefox.get('https://www.crunchbase.com/organization/apple')
    except:
        pass
    driver.get('https://techcrunch.com/')
    firefox.set_page_load_timeout(2)
    driver.set_page_load_timeout(30)

def existence_in_crunchbase(name):
    #test : https://www.crunchbase.com/app/search?q=neokami
    base_url = 'www.crunchbase.com'
    url = 'https://techcrunch.com/search/'+name
    url_crunchbase = None
    try:
        driver.get(url)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('timeout of phantomjs')
        pass
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    blocks = soup.select("h2.post-title a")
    if len(blocks)>0:
        url_crunchbase = blocks[0]["href"]  
        name  = blocks[0].getText()
 
        if base_url not in url_crunchbase:
            url_crunchbase = None
    
    return url_crunchbase
            

def extract_company_techcrunch(name,url):
    try:
        firefox.get(url)
    except:
        pass
    founded = None
    employees = None
    website = None
    company_name = ''
    blocks_dt = []
    blocks_dd = []
    blocks_dt_site = []
    blocks_dd_site = []
    try:
        soup = BeautifulSoup(firefox.page_source, "html.parser")
        blocks_dt = soup.select("div.details dt")
        blocks_dd = soup.select("div.details dd")
        blocks_dt_site = soup.select("div.container dt")
        blocks_dd_site = soup.select("div.container dd")
        company_name_tag = soup.select_one("#profile_header_heading")
        if company_name_tag == None:
            company_name = ''
        else:
            company_name = company_name_tag.getText()
    except:
        pass

    i = 0
    while company_name.lower() != name.lower() or len(blocks_dt)==0 or len(blocks_dt_site)==0 :
        time.sleep(0.3)
        try:
            soup = BeautifulSoup(firefox.page_source, "html.parser")
            company_name_tag = soup.select_one("#profile_header_heading")
            if company_name_tag:
                company_name = company_name_tag.getText()
            else:
                company_name = ''
            blocks_dt = soup.select("div.details dt")
            blocks_dd = soup.select("div.details dd")
            blocks_dt_site = soup.select("div.container dt")
            blocks_dd_site = soup.select("div.container dd")
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass
        i=i+1
        if i >= 100:
            print('fail to crawl ', name , ' in crunchbase')
            break

    
    if company_name.lower() == name.lower() and len(blocks_dt)>0:
        for index_1,block_1 in enumerate(blocks_dt):
            if 'Founded' in  block_1.getText() : 
                founded = blocks_dd[index_1].getText()
            if 'Employees' in block_1.getText():
                employees = blocks_dd[index_1].getText().split('|')[0]
    if company_name.lower() == name.lower() and len(blocks_dt_site)>0:
        if len(blocks_dt_site) == len(blocks_dd_site):           
            for index_2, block_2 in enumerate(blocks_dt_site):
                if 'Website' in block_2.getText():
                    website = blocks_dd_site[index_2].getText()
        else: 
            for index, block_3 in enumerate(blocks_dd_site):
                if 'http' in block_3.getText():
                    website = block_3.getText()
                    
    #print(founded, employees, website)
    return founded,employees,website

#extract_company_techcrunch("JetSmarter", "https://www.crunchbase.com/organization/jetsmarter#/entity")