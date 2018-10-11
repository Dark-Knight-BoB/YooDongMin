import requests
from bs4 import BeautifulSoup as bs
import Crawler as cr
from pprint import pprint
from time import sleep
import re
loginPage = 'http://highkorea5ou4wcy.onion/ucp.php?mode=login'
ID = 'michin'
passwd = 'michin'
highkorea='http://highkorea5ou4wcy.onion'

LOGIN_INFO = {
    'username' : ID,
    'password' : passwd
}
sIDpat= re.compile('sid=(.*?);')
with requests.session() as s:
    s.proxies = {}
    s.proxies['http'] = 'socks5h://localhost:9050'
    s.proxies['https'] = 'socks5h://localhost:9050'

    r = s.get(loginPage)

    html = r.text

    soup = bs(html, 'html.parser')

    sid = soup.find('input', {'name':'sid'}).get('value')
'''
    LOGIN_INFO['sid'] = sid

    r = s.post(loginPage, data= LOGIN_INFO)

    html = r.text

    soup = bs(html, 'html.parser')

    print(soup)
'''
'''
    req = s.get(highkorea)
    
    html = req.text

    status = req.status_code

    soup = bs(html, 'html.parser')

    mainCategory = soup.find_all("a", {"class": "topictitle"})
    for category in mainCategory:
        print("Forum : {}".format(category.text))
'''

'''
    cookie = r.headers['Set-Cookie']
    m = sIDpat.search(cookie)
    r = s.get(highkorea + '&sid=' + m.group(1))
    print(cookie == r.headers['Set-Cookie'])

'''



'''
    header = {'Server': 'nginx',
                'Date': 'Thu, 11 Oct 2018 02:03:33 GMT',
                'Content-Type': 'text/html; charset=UTF-8',
                'Transfer-Encoding': 'chunked',
                'Connection': 'keep-alive',
                'X-Powered-By': 'PHP/5.5.9-1ubuntu4.9',
                'Set-Cookie':'phpbb3_d7j2o_u=1; '
                            'expires=Fri, 11-Oct-2019 02:03:33 GMT; '
                            'path=/; domain=highkorea5ou4wcy.onion; '
                            'HttpOnly, phpbb3_d7j2o_k=; '
                            'expires=Fri, 11-Oct-2019 02:03:33 GMT; '
                            'path=/; domain=highkorea5ou4wcy.onion; '

                            'HttpOnly, phpbb3_d7j2o_sid=d8054f73806238e5c03b790abb866065; '
                            'expires=Fri, 11-Oct-2019 02:03:33 GMT; '
                            'path=/; domain=highkorea5ou4wcy.onion; '

                            'HttpOnly',

                'Cache-Control': 'private, no-cache="set-cookie"',
                'Expires': '0',
                'Pragma': 'no-cache',
                'Content-Encoding': 'gzip',
                'Vary': 'Accept-Encoding'}
'''
