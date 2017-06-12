import os
import json
from dateutil.parser import parse

'''
if os.path.isfile("raw_companies.json"):
	f=open("raw_companies.json")
	company = json.load(f)
	f.close()
	for index, company in enumerate(company):
		if company['name'] == "British Airways":
			print(index)

'''

'''
# check if there are articles without date
if os.path.isfile("data.json"):
	file = open("data.json")
	raw_data = json.load(file)
	file.close()
	for index, article in enumerate(raw_data['techInsider']):
		if(article['date'] == None):
			print(index, article['origin'])
			
'''

'''
date1 = int(parse("16th May 17").timestamp())
date2 = int(parse("20th Mar 17").timestamp())
if date1 > date2:
	print("false")
else:
	print("true")
'''

# get the last crawled articles timestamps, add in crawler.crawl() function
timestamp = {}
if os.path.isfile("data.json"):
	file = open("data.json")
	raw_data = json.load(file)
	file.close()
	for key, value in raw_data.items():
		timestamp[key] = 0
		for index, article in enumerate(raw_data[key]):
			if int(article['date']) > int(timestamp[key]):
				timestamp[key] = article['date']
	print(timestamp)
	with open('timestamps.json', 'w') as f:
		json.dump(timestamp, f, indent=2)
		f.close()
		



			
			
