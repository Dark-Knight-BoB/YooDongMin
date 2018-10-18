import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
import time
from multiprocessing import Pool
from itertools import repeat
from collections import OrderedDict

#with open('/home/kyw/highkorea/highkoreathesis.txt', 'w') as wf:
def highkorealogin(login_info, object):
    LOGIN_INFO=login_info
    highkorea = object
    with requests.session() as s:
        tup = highkorea.staticGet(s, loginPage)
        s, soup = tup[0], tup[2]

        # Login
        sid = soup.find('input', {'name': 'sid'})
        redirect = soup.find('input', {'name': 'redirect'})
        login = soup.find('input', {'name': 'login'})
        LOGIN_INFO = dict(LOGIN_INFO, **{'sid': sid['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'redirect': redirect['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'login': login['value']})
        s = highkorea.staticPost(s, loginPage, LOGIN_INFO)[0]
    return s, highkorea
    # Main Page

def getForums(session, object, url):
    highkorea = object
    s = session
    tup = highkorea.staticGet(s, url)
    s, soup = tup[0], tup[2]
    forums = soup.find_all("a", {"class": "forumtitle"})
    forumtitles = [forum.text for forum in forums]
    forumURLs=[forum.get('href') for forum in forums]
    return s, forumtitles, forumURLs


def getLastPage(session, object, forumtitles,  forumurls):
    lastpages=dict()
    highkorea = object
    s = session
    for title, url in zip(forumtitles, forumurls):
        forumurl = highkorea.stem + url.strip('.')
        tup = highkorea.staticGet(s, forumurl)
        s, soup = tup[0], tup[2]
        lastpg = soup.select(
            'div.topic-actions div span a'
        )
        lastpage = lastpg[-1].get('href') if lastpg != [] else soup.select('#page-body h2 a')[0].get('href')
        lastpages[title]=lastpage
    return s, lastpages
    # soup.select('#page-body h2 a')

def getContents(session, object, forumurl):
    highkorea = object
    s = session
    tup = highkorea.staticGet(s, forumurl)
    s, soup = tup[0], tup[2]
    titles = soup.find_all("a", {"class": "topictitle"})
    dates = soup.select(
        'li.announce dl dd span'
    )
    for date in dates:
        print(date)
'''
    for title in titles:
        titleURL = title.get('href')
        tup = highkorea.staticGet(s, highkorea.stem + titleURL.strip('.'))
        lastpg = soup.select(
            'div.topic-actions div span a'
        )

        contents = soup.find_all("div", {"class": "content"})
        authors = soup.find_all("a",{"class": "username-coloured"})

        for content in contents:
            ct = content.get_text()
'''

#http: // highkorea5ou4wcy.onion / viewforum.php?f = 34 & start = 23

if __name__=='__main__':
    loginPage = 'http://highkorea5ou4wcy.onion/ucp.php?mode=login'
    mainpage = 'http://highkorea5ou4wcy.onion'

    ID = 'michin'
    passwd = 'michin'

    LOGIN_INFO = {
        'username': ID,
        'password': passwd
    }

    start_time = time.time()
    print("--- %s seconds ---" % time.time())
    highkorea = cr.Site(mainpage)

    print("--- %s seconds ---" % time.time())
    session = highkorealogin(LOGIN_INFO, highkorea)[0]
    print("--- %s seconds ---" % time.time())
    tup = getForums(session, highkorea, highkorea.stem)
    session, forumtitles, forumurls = tup[0], tup[1], tup[2]
    tup=getLastPage(session, highkorea, forumtitles, forumurls)
    session, lastpages = tup[0],tup[1]
    
    #pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.

    #pool.starmap(getLastPage, zip(repeat(s), repeat(highkorea), tup[1], tup[2], lastpagelst))
    print("--- %s seconds ---" % (time.time() - start_time))
#cr.mkjson(totaldata, '/home/kyw/json_datas', '20181014_thesis_highkorea.json')
