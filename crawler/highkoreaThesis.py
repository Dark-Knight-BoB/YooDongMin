import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
from pprint import pprint
from time import sleep
import re
loginPage = 'http://highkorea5ou4wcy.onion/ucp.php?mode=login'
ID = 'michin'
passwd = 'michin'
highkoreaURL='http://highkorea5ou4wcy.onion'

LOGIN_INFO = {
    'username' : ID,
    'password' : passwd
}

totaldata=[]

with open('/home/kyw/highkorea/highkoreathesis.txt', 'w') as wf:

    with requests.session() as s:
        highkorea = cr.Site(highkoreaURL)
        s, soup = highkorea.staticGet(s, loginPage)[0], highkorea.staticGet(s, loginPage)[2]

        # Login
        sid = soup.find('input', {'name': 'sid'})
        redirect = soup.find('input', {'name': 'redirect'})
        login = soup.find('input', {'name': 'login'})
        LOGIN_INFO = dict(LOGIN_INFO, **{'sid': sid['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'redirect': redirect['value']})
        LOGIN_INFO = dict(LOGIN_INFO, **{'login': login['value']})
        s = highkorea.staticPost(s, loginPage, LOGIN_INFO)[0]

        # Main Page
        s, soup = highkorea.staticGet(s, highkorea.stem)[0], highkorea.staticGet(s, highkorea.stem)[2]
        mainforums = soup.find_all("a", {"class": "forumtitle"})

        for mainforum in mainforums:
            print("Forum : {}".format(mainforum.text))
            forumUrl = mainforum.get('href')
            s, soup = highkorea.staticGet(s, highkorea.stem + forumUrl.strip('.'))[0], highkorea.staticGet(s, highkorea.stem + forumUrl.strip('.'))[2]
            titles = soup.find_all("a", {"class": "topictitle"})

            for title in titles:
                titleURL = title.get('href')
                s, soup = highkorea.staticGet(s, highkorea.stem + titleURL.strip('.'))[0], highkorea.staticGet(s, highkorea.stem + titleURL.strip('.'))[2]
                contents = soup.find_all("div", {"class": "content"})
                for content in contents:
                    ct = content.get_text()
                    wf.write(ct)


  #         authors = soup.find_all("a",{"class": "username-coloured"})

    #        for author, title in zip(authors, titles):

                '''
                data = dict()
                data['author'] = author
                data['title'] = title
                data['content'] = []
'''
#                    data['content'].append(ct)
#                totaldata.append(data)

'''
        authors = soup.find_all("a",{"class": "username-coloured"})
'''

        #ddd= soup.find("dd", {"class":"lastpost"})
        #for title, author in zip(titles, authors):
        #    print("{} : {}".format(title.text, author.text))

#cr.mkjson(totaldata, '/home/kyw/json_datas', '20181014_thesis_highkorea.json')
