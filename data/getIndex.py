import os
import json

if os.path.isfile("raw_companies.json"):
	f=open("raw_companies.json")
	company = json.load(f)
	f.close()
	for index, company in enumerate(company):
		if company['name'] == "British Airways":
			print(index)