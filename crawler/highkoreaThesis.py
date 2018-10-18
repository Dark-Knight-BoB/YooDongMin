import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
import time
from multiprocessing import Pool
from itertools import repeat


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


def getTitles(session, object, forumUrl):
    highkorea = object
    s = session
    forumurl = highkorea.stem + forumUrl.strip('.')
    tup = highkorea.staticGet(s, forumurl)
    s, soup = tup[0], tup[2]
    #lastpage = soup.find('span', {"class":"page-dots"}).next_element
    titles = soup.find_all("a", {"class": "topictitle"})
    print(titles)
    #print(lastpage)
    '''
    for title in titles:
        titleURL = title.get('href')
        s, soup = highkorea.staticGet(s, highkorea.stem + titleURL.strip('.'))[0], highkorea.staticGet(s, highkorea.stem + titleURL.strip('.'))[2]
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
    print(time.time())
#    totaldata = []
    highkorea = cr.Site(mainpage)

    print(time.time())
    # present_link = get_links()
    # new_html = compare_number(present_link.strip('.html'), output)
    session = highkorealogin(LOGIN_INFO, highkorea)[0]
    print(time.time())
    tup = getForums(session, highkorea, highkorea.stem)
    #print(tup[1])
#    for forum in tup[2]:
#        getTitles(tup[0], highkorea, forum)
    s = tup[0]

    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    pool.starmap(getTitles, zip(repeat(s), repeat(highkorea), tup[2]))
#    agoraCrawler(new_html)
    print("--- %s seconds ---" % (time.time() - start_time))


#cr.mkjson(totaldata, '/home/kyw/json_datas', '20181014_thesis_highkorea.json')
