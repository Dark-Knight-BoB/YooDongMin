import requests
import re
import json
from collections import OrderedDict
from bs4 import BeautifulSoup as bs
from urllib import urlopen

allExtLinks = OrderedDict()
allExtLinks["ExtLinks"] = []

def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getAllExternalLinks(siteUrl,keyword):
    html = urlopen(siteUrl)
    bsObj = bs(html, "html.parser")
    externalLinks = getExternalLinks(bsObj,splitAddress(domain)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.setdefault(keyword,[]).append(link)
            print(link)

keyword = [ "northkorea" , "drug"] # 검색할 

for search in keyword: #keyword search
	print("Searching : "+search)
	page = 1
	html = urlopen("http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page=1")
	soup = bs(html,'html.parser')
	content = soup.find_all('div',{'class':'ruler'})
        if(content):
            print("PAGE : 1")
            domain = "http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page="+str(page)
	    getAllExternalLinks(domain,search)
        else:
            while page < 20: #page loop
                print("PAGE : "+ str(page) )
                domain = "http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page="+str(page)
		getAllExternalLinks(domain,search)
		page += 1
	with open('allExtLinks.json', 'w', encoding="utf-8") as make_file:
		json.dump(allExtLinks, make_file, ensure_ascii=False, indent="\t")
