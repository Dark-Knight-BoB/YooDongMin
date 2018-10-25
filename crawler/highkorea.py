import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
import time
from multiprocessing import Pool
from itertools import repeat
from collections import OrderedDict
import re
import datetime



def highkorealogin(login_info, object,loginpage):
    LOGIN_INFO=login_info
    highkorea = object
    with requests.session() as s:
        tup = highkorea.staticGet(s, loginpage)
        s, soup = tup[0], tup[2]

        # Login
        sid = soup.find('input', {'name': 'sid'})
        redirect = soup.find('input', {'name': 'redirect'})
        login = soup.find('input', {'name': 'login'})
        LOGIN_INFO = dict(LOGIN_INFO, **{'sid': sid['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'redirect': redirect['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'login': login['value']})
        time.sleep(1)
        s = highkorea.staticPost(s, loginpage, LOGIN_INFO)[0]
    return s
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


def getTitles(session, object, forumurl):
    error_data=list()
    data = list()
    highkorea = object
    s = session
    m = re.compile('&start=(\d+)').search(forumurl)
    num = 1
    datPat = re.compile(
        '\(.\) (?P<month>\d{2}) (?P<day>\d{2}), (?P<year>\d{4}) (?P<hour>\d{1,2}):(?P<minute>\d{2}) (?P<noon>[a-z]{2})')
    if m:
        num = int(m.group(1))
        url = re.sub('&start=(\d+)','',forumurl)
    else:
        url = forumurl
    for i in range(0, num, 25):
        tup = highkorea.staticGet(s, highkorea.stem + url.strip('.')+'&start={}'.format(i))
        s, soup = tup[0], tup[2]
        titles = soup.find_all("a", {"class": "topictitle"})
        dates = soup.find_all("dd", {"class": "lastpost"})
        authors = soup.select(
            'li.row dl dt a.username-coloured'
        )
        year, month, day, hour, minute, noon, unixtime = '', '', '', '', '', '', 0
        for date, tempTitle, tempAuthor in zip([date.text for date in dates], titles, authors):
            article = OrderedDict()
            m = datPat.search(date)
            try:
                titleURL = tempTitle.get('href')
                title = tempTitle.text
                author = tempAuthor.text
                if m:
                    month, day, year, hour, minute, noon = m.group("month"),m.group("day"), m.group("year"), m.group("hour"), m.group("minute"),m.group("noon")
                    hour = int(hour) + 12 if noon == 'pm' else int(hour)
                    d = datetime.datetime(int(year),int(month),int(day), hour, int(minute))
                    unixtime = int(time.mktime(d.timetuple()))
                else:
                    error_data.append(titleURL)
                article['titleURL']=titleURL
                article['title']=title
                article['author']=author
                article['lastup']=unixtime
                data.append(article)
            except:
                error_data.append(tempTitle.get('href'))
    cr.mkjson(error_data, '/json_datas/highkorea','hkTitle_error.json')
    return data


def getContent(session, object, title):
    error_data = OrderedDict()
    return_data = OrderedDict()

    highkorea = object
    s = session
    topicurl = title['titleURL']
    topictitle = title['title']
    topicauthor = title['author']
    lastup = title['lastup']
    try:
        tup = highkorea.staticGet(s, highkorea.stem + topicurl.strip('.'))
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
        html_datas=list()
        image_datas = list()
        for i in range(0, num, 10):
            tup = highkorea.staticGet(s, highkorea.stem + url.strip('.') + '&start={}'.format(i))
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
        return_data['image'] = image_datas
        return_data['html'] = html_datas
        return_data['content'] = content_datas
        return_data['url'] = topicurl
        return_data['title'] = topictitle
        return_data['author'] = topicauthor
        return_data['lastup'] = lastup
        # return_data[topicurl] = return_data
        return return_data
    except Exception as e:
        error_data[title['titleURL']] = e
        cr.mkjson(error_data, '/json_datas/highkorea', 'hkContent_error.json')
        pass


if __name__=='__main__':
    tod = datetime.date.today()
    todstr = tod.isoformat()
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
    session = highkorealogin(LOGIN_INFO, highkorea, loginPage)
    tup = getForums(session, highkorea, highkorea.stem)
    session, forumtitles, forumurls = tup[0], tup[1], tup[2]
    tup=getLastPage(session, highkorea, forumtitles, forumurls)
    session, lastpages = tup[0],tup[1]
    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    results = pool.starmap(getTitles, zip(repeat(session), repeat(highkorea), lastpages.values()))
    cr.mkjson(results, '/json_datas', 'hkTitle.json')
    for i, forum in enumerate(results):
        content = list()
        pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
        results = pool.starmap(getContent, zip(repeat(session), repeat(highkorea), forum))
        cr.mkjson(results, '/json_datas/highkorea', '{}_hkContent.json'.format(i))  # 2018-10-21_1_hkContent.json
