import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from pyvirtualdisplay import Display
from selenium import webdriver
import Crawler as cr
agora='http://c2djzrn6qx6kupkn.onion/'

agora = cr.Site(agora)
soup = agora.staticReq(agora.stem)
print(soup)
'''
messages = soup.find_all("div", {"class":"message"})
for message in messages:
    print(message.get_text())
'''