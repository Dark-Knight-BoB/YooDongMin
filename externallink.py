import requests
from bs4 import BeautifulSoup as bs
from urllib import urlopen
import re

pages = set()

def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks
 
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

allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = bs(html, "html.parser")
    internalLinks = getInternalLinks(bsObj,splitAddress(domain)[0])
    externalLinks = getExternalLinks(bsObj,splitAddress(domain)[0])
 
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

domain = 'http://zlal32teyptf4tvi.onion'
getAllExternalLinks(domain)

