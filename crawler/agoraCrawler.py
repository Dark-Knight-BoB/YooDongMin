#-*-coding:utf-8-*-
import requests, json
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
#from pyvirtualdisplay import Display
#from selenium import webdriver
import Crawler as cr
agora='http://c2djzrn6qx6kupkn.onion/'
#datas = list()


with requests.Session() as s:
    agora = cr.Site(agora)
    for i in range(1,862):
        s, soup = agora.staticGet(s, agora.stem+ "/{}.html".format(i))[0], agora.staticGet(s, agora.stem + "/{}.html".format(i))[2]
        messages = soup.find_all("div", {"class": "message"})
        labels = soup.find_all("label")
        ids = soup.find_all("span", {"class": "reflink"})
        for id , label, message in zip(ids, labels, messages):
            posterman = label.find("span", {"class": "postername"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "postername"}) is not None else None
            filetitle = label.find("span", {"class": "filetitle"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "filetitle"}) is not None else None
            for lab in label("span"):
                lab.decompose()
            mid = id.find_all('a')[-1].get_text()
            date = label.get_text().encode('iso-8859-1').decode('utf-8').strip('\n').strip('  ')
            ms = message.get_text().encode('iso-8859-1').decode('utf-8').strip('\n')


'''
    data = OrderedDict()
    data['id'] = id.find_all('a')[-1].get_text()
    data['date'] = date.get_text()
    data['message'] = message.get_text()
    datas.append(data)
'''

#cr.mkjson('/home/kyw/json_datas/', datas)
