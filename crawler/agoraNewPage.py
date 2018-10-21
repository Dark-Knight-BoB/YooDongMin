#-*-coding:utf-8-*-
import requests, json
import Crawler as cr
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import subprocess
import re
import time
import datetime
#from pyvirtualdisplay import Display1
#from selenium import webdriver
#datas = list()
#with open('/home/kyw/highkorea/agora.txt', 'w+') as wf:


def get_link():
    with open('/home/kyw/agoraHTMLnumber/agoraHTMLnumber.txt', 'a') as wf:
        agora = 'http://c2djzrn6qx6kupkn.onion/'
        with requests.Session() as s:
            agora = cr.Site(agora)
            tup = agora.staticGet(s, agora.stem)
            s, html = tup[0], tup[1]
            links = re.compile('href="(\d+\.html)').findall(html.text)
            wf.write(links[-1].strip('.html')+'\n')
    return links[-1]


def compare_number(present_link, last_link):
    try:
        new_html = int(present_link) - int(last_link)
    except ValueError:
        new_html = int(present_link) - 0
    return new_html
'''
def agoraCrawler(new_html):
    with requests.Session() as s:
        agora = 'http://c2djzrn6qx6kupkn.onion/'
        agora = cr.Site(agora)
        #soup=''
        for i in range(new_html+1):
            if i == 0:
                tup = agora.staticGet(s, agora.stem)
                s, soup = tup[0], tup[2]
            else:
                tup = agora.staticGet(s, agora.stem + "/{}.html".format(i))
                s, soup = tup[0], tup[2]
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
                print(posterman)
'''

def agoraMultiCrawler(new_html):

    with requests.Session() as s:

        return_data = OrderedDict()
        agora = 'http://c2djzrn6qx6kupkn.onion/'
        agora = cr.Site(agora)

        # if i == 0:
        #     tup = agora.staticGet(s, agora.stem)
        #     s, html, soup = tup[0], tup[1].text, tup[2]
        tup = agora.staticGet(s, agora.stem + "/{}.html".format(new_html))
        s, html, soup = tup[0], tup[1].text, tup[2]
        messages = soup.find_all("div", {"class": "message"})
        labels = soup.find_all("label")

        ids = soup.find_all("span", {"class": "reflink"})

        content_data = list()

        for id , label, message in zip(ids, labels, messages):
            temp_data = OrderedDict()
            posterman = label.find("span", {"class": "postername"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "postername"}) is not None else None
            filetitle = label.find("span", {"class": "filetitle"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "filetitle"}) is not None else None
            for lab in label("span"):
                lab.decompose()
            mid = id.find_all('a')[-1].get_text()
            date = label.get_text().encode('iso-8859-1').decode('utf-8').strip('\n').strip('  ')
            ms = message.get_text().encode('iso-8859-1').decode('utf-8').strip('\n')
            temp_data['author']=posterman
            temp_data['title']=filetitle
            temp_data['id']=mid
            temp_data['date']=date
            temp_data['message']=ms
            content_data.append(temp_data)
        return_data['html'] = html
        return_data['content'] = content_data
        return_data['url'] = tup[1].url
        return return_data


def agoraStemCrawler():
    with requests.Session() as s:

        return_data = OrderedDict()
        agora = 'http://c2djzrn6qx6kupkn.onion/'
        agora = cr.Site(agora)
        tup = agora.staticGet(s, agora.stem)
        s, html, soup = tup[0], tup[1].text, tup[2]
        messages = soup.find_all("div", {"class": "message"})
        labels = soup.find_all("label")

        ids = soup.find_all("span", {"class": "reflink"})

        content_data = list()

        for id , label, message in zip(ids, labels, messages):
            temp_data = OrderedDict()
            posterman = label.find("span", {"class": "postername"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "postername"}) is not None else None
            filetitle = label.find("span", {"class": "filetitle"}).get_text().encode('iso-8859-1').decode('utf-8').strip('\n') if label.find("span", {"class": "filetitle"}) is not None else None
            for lab in label("span"):
                lab.decompose()
            mid = id.find_all('a')[-1].get_text()
            date = label.get_text().encode('iso-8859-1').decode('utf-8').strip('\n').strip('  ')
            ms = message.get_text().encode('iso-8859-1').decode('utf-8').strip('\n')
            temp_data['author']=posterman
            temp_data['title']=filetitle
            temp_data['id']=mid
            temp_data['date']=date
            temp_data['message']=ms
            content_data.append(temp_data)
        return_data['html'] = html
        return_data['content'] = content_data
        return_data['url'] = tup[1].url
        return return_data



if __name__=='__main__':
    start_time = time.time()
    output = subprocess.check_output(['tail', '-n 1', '/home/kyw/agoraHTMLnumber/agoraHTMLnumber.txt'], universal_newlines=True)
    present_link = get_link()
    new_html = compare_number(present_link.strip('.html'), output)
    total_data=list()
    data = agoraStemCrawler()
    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    datas = pool.map(agoraMultiCrawler, range(new_html+1))
    datas.append(data)
    print("--- %s seconds ---" % (time.time() - start_time))
    cr.mkjson(datas, '/home/kyw/json_datas/agora', 'agora.json')
