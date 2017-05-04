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

		self.firefox_capabilities = DesiredCapabilities.FIREFOX
		self.firefox_capabilities['marionette'] = True
		self.firefox_capabilities['handleAlerts'] = True
		self.firefox_capabilities['acceptSslCerts'] = True
		self.firefox_capabilities['acceptInsecureCerts'] = True
		self.geckoPath = 'geckodriver.exe'
		self.browser = webdriver.Firefox(capabilities=self.firefox_capabilities, executable_path=self.geckoPath)
		
		
	def crawl(self):
		links = []
		self.browser.get(self.base_url)
		for i in range(self.number_of_pages_to_crawl):
			time.sleep(0.5)
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		page_of_link = BeautifulSoup(self.browser.page_source, "html.parser")
		blocks = page_of_link.select("article div.post-list__left a.post-list__image")
		for block in blocks:
			link = block["href"]  # url
			links.append(link)	
		print("number of links : ",len(links))

		for i,link in enumerate(links,1):
			content = ""
			print(i," : link",link)
			self.browser.get(link)
			page = BeautifulSoup(self.browser.page_source, "html.parser")
			paragraphs = page.select("div.clearfix p")
			for paragraph in paragraphs:
				content += paragraph.getText()

			try:
				date = page.find("meta",  property="article:modified_time")
				date = date["content"]
				date = int(parse(date).timestamp())
			except TypeError:
				date = str(0)
			except AttributeError:
				date = str(0)
			title = page.select_one("title").getText()
			article = {
				"title": title,
				"content": content,
				"date": date,
				"url": link,
				"origin": "startupuk"
			}
			if len(content) <=1000:
				print("content is not enough or something goes wrong of this link : ", link)
			else:
				self.articles.append(article)
		self.browser.quit()
		with open('teckinasia.json', 'w') as f:
			json.dump(self.articles, f)

	def get_articles(self):
		return self.articles

	def log(self, message):
		if not self.silent:
			print(message)









