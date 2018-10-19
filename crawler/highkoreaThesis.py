import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
import time
from multiprocessing import Pool
from itertools import repeat
from collections import OrderedDict
import re
import datetime
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
        time.sleep(1)
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
    lastpages=OrderedDict()
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

def getTitles(session, object, forumurl):
    data = list()
    highkorea = object
    s = session
    url=re.sub('start=\d+','start=',forumurl)
    for i in range(0, int(forumurl[-2])+1, 25):
        tup = highkorea.staticGet(s, highkorea.stem + url.strip('.')+str(i))
        s, soup = tup[0], tup[2]

        titles = soup.find_all("a", {"class": "topictitle"})
        dates = soup.find_all("dd", {"class": "lastpost"})
        authors = soup.select(
            'li.row dl dt a.username-coloured'
        )
        datPat=re.compile('\(.\) (?P<month>\d{2}) (?P<day>\d{2}), (?P<year>\d{4}) (?P<hour>\d{1,2}):(?P<minute>\d{2}) (?P<noon>[a-z]{2})')

        for date, tempTitle, tempAuthor in zip([date.text for date in dates if '게시글' not in date.text], titles, authors):
            article = dict()
            m = datPat.search(date)
            year, month, day, hour, minute, noon, unixtime='','','','','','',0
            if m:
                month, day, year, hour, minute, noon = m.group("month"),m.group("day"), m.group("year"), m.group("hour"), m.group("minute"),m.group("noon")
                hour = int(hour) + 12 if noon == 'pm' else int(hour)
                d = datetime.datetime(int(year),int(month),int(day), hour, int(minute))
                unixtime = int(time.mktime(d.timetuple()))
            else:
                print(date)
            titleURL = tempTitle.get('href')
            title = tempTitle.text
            author = tempAuthor.text
            article['titleURL']=titleURL
            article['title']=title
            article['author']=author
            article['lastup']=unixtime
            data.append(article)
    return data

'''

        contents = soup.find_all("div", {"class": "content"})
        authors = soup.find_all("a",{"class": "username-coloured"})

        for content in contents:
            ct = content.get_text()
'''


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
    highkorea = cr.Site(mainpage)
    session = highkorealogin(LOGIN_INFO, highkorea)[0]
    print("--- %s seconds ---" % time.time())
    tup = getForums(session, highkorea, highkorea.stem)
    session, forumtitles, forumurls = tup[0], tup[1], tup[2]
    tup=getLastPage(session, highkorea, forumtitles, forumurls)
    session, lastpages = tup[0],tup[1]

    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.

    results = pool.starmap(getTitles, zip(repeat(session), repeat(highkorea), lastpages.values()))
    outputs = [result[0] for result in results]

    print("--- %s seconds ---" % (time.time() - start_time))
    cr.mkjson(outputs, '/home/kyw/json_datas', '20181019_thesis_highkorea.json')
