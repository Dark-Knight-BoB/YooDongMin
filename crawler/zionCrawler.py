import Crawler as cr
import requests, json, os
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from itertools import repeat
from collections import OrderedDict
import re
import datetime,time
import hkTitleCrawl as hktc

def zionlogin(login_info, object,loginpage):
    LOGIN_INFO=login_info
    zion = object
    with requests.session() as s:
        tup = zion.staticGet(s, loginpage)
        s, soup = tup[0], tup[2]

        # Login
        sid = soup.find('input', {'name': 'sid'})
        redirect = soup.find('input', {'name': 'redirect'})
        login = soup.find('input', {'name': 'login'})
        LOGIN_INFO = dict(LOGIN_INFO, **{'sid': sid['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'redirect': redirect['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'login': login['value']})
        time.sleep(1)
        s = zion.staticPost(s, loginpage, LOGIN_INFO)[0]
    return s

def getLastPage(session, object, forumtitles,  forumurls):
    lastpages=OrderedDict()
    zion = object
    s = session
    for title, url in zip(forumtitles, forumurls):
        forumurl = zion.stem + url.strip('.')
        tup = zion.staticGet(s, forumurl)
        s, soup = tup[0], tup[2]
        lastpg = soup.find_all("a", {"class" : "button", "role":"button"})


        lastpage = lastpg[-1].get('href') if lastpg != [] else soup.select('#page-body h2 a')[0].get('href')
        lastpages[title]=lastpage
    return s, lastpages

def getTitles(session, object, forumurl):
    error_data=list()
    data = list()
    zion = object
    s = session
    m = re.compile('&start=(\d+)').search(forumurl)
    num = 1
    if m:
        num = int(m.group(1))
        url = re.sub('&start=(\d+)','',forumurl)
    else:
        url = forumurl
    for i in range(0, num, 25):
        tup = zion.staticGet(s, zion.stem + url.strip('.')+'&start={}'.format(i))

        s, soup = tup[0], tup[2]
        if i == 0:
            forums = soup.find_all("a", {"class": "forumtitle"})
            if forums != []:
                forumURLs = [forum.get('href') for forum in forums]
                forumtitles = [forum.text for forum in forums]
                tup = getLastPage(s, zion, forumtitles, forumURLs)
                for x in tup[1].values():
                    internal_data = getTitles(s, zion, x)
                    data.extend(internal_data)
        titles = soup.find_all("a", {"class": "topictitle"})
        authors = soup.find_all("a", {"class": "username"}) if soup.find_all("a", {"class": "username"}) != [] else soup.find_all("a", {"class": "username-coloured"})

        for tempTitle, tempAuthor in zip(titles, authors):
            article = OrderedDict()
            try:
                titleURL = tempTitle.get('href')
                title = tempTitle.text
                author = tempAuthor.text
                article['titleURL']=titleURL
                article['title']=title
                article['author']=author
                data.append(article)
            except:
                error_data.append(tempTitle.get('href'))
    if data == []:
        cr.mktxt(forumurl + '\n', '/home/kyw/json_datas/zion', 'zion_noTitle.txt')
    return data

def getContent(session, object, title):
    return_data = OrderedDict()
    error_data = OrderedDict()
    zion = object
    s = session
    topicurl = title['titleURL']

    tup = zion.staticGet(s, zion.stem + topicurl.strip('.'))
    s, html, soup = tup[0], tup[1].text, tup[2]
    lastpg = soup.select('div.topic-actions div span a')
    lastpage = lastpg[-1].get('href') if lastpg != [] else soup.select('#page-body h2 a')[0].get('href')
    m = re.compile('&start=(\d+)').search(lastpage)
    num = 1
    if m:
        num = int(m.group(1))
        url = re.sub('&start=(\d+)', '', lastpage)
    else:
        url = lastpage
    content_datas=list()
    temp_data=OrderedDict()
    html_datas=list()
    image_datas = list()
    for i in range(0, num, 10):
        tup = zion.staticGet(s, zion.stem + url.strip('.') + '&start={}'.format(i))
        s, html, soup = tup[0], tup[1].text, tup[2]
        authors = soup.select(".author strong a.username-coloured")
        contents = soup.find_all('div', {'class':'content'})
        images = soup.select('dl.attachbox dd dl dt a img')
        for author, content in zip(authors, contents):
            content_data=OrderedDict()
            for br in content.find_all('br'):
                br.replace_with('\n')
            content_data['author']=author.text
            content_data['content']=content.text
            content_datas.append(content_data)
        for image in images:
            image_data = OrderedDict()
            image_data['src'] = image.get('src')
            image_data['name'] = image.get('alt')
            image_datas.append(image_data)
        html_datas.append(html)
    temp_data['image'] = image_datas
    temp_data['html'] = html_datas
    temp_data['content'] = content_datas
    return_data[topicurl] = temp_data
    return return_data
    # except Exception as e:
    #     error_data[title['titleURL']] = e
    #     cr.mkjson(error_data, '/home/kyw/json_datas/zion', 'zion_Content_error.json')
    #     pass

if __name__=='__main__':
    mainpage = 'http://hzionerlko3on77m.onion'
    loginPage = 'http://hzionerlko3on77m.onion/ucp.php?mode=login'
    zion = cr.Site(mainpage)
    ID = 'chickenS2'
    passwd = 'chickenS2'
    LOGIN_INFO = {
        'username': ID,
        'password': passwd
    }
    start_time = time.time()
    session = zionlogin(LOGIN_INFO, zion, loginPage)
    print(time.time() - start_time)
    tup = hktc.getForums(session, zion, zion.stem)
    session, forumtitles, forumurls = tup[0], tup[1], tup[2]
    tup=getLastPage(session, zion, forumtitles, forumurls)
    session, lastpages = tup[0],tup[1]
    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    results = pool.starmap(getTitles, zip(repeat(session), repeat(zion), lastpages.values()))
    cr.mkjson(results, '/home/kyw/json_datas/zion', 'zion_Title.json')
    for i, title in enumerate(results):
        contents = pool.starmap(getContent, zip(repeat(session), repeat(zion), title))
        print(contents)
        # cr.mkjson(results, '/home/kyw/json_datas/zion', '{}_zion_Content.json'.format(i))  # 2018-10-21_1_hkContent.json




