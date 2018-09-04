# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import json
import os

# 현재 python 파일의 위치 => 현재 경로의 디렉토리를 얻어오는 함수 (아마도 맞을듯함)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 크롤 대상의 주소 가져오기
headers={'User-Agent': 'Mozilla/5.0'}
stemURL = 'http://manpd.tistory.com'
req = requests.get('http://manpd.tistory.com/category', headers = headers)

# 대상의 HTML 소스코드 가져오기
html = req.text
header = req.headers
status = req.status_code

soup = bs(html, 'html.parser')

my_pages = soup.select(
    '#paging > span > a'
)
LastPage = my_pages[-1].get('href')
GetLastPage=LastPage

# 마지막 페이지 얻기
while True:
    req = requests.get(stemURL + LastPage, headers=headers)
    html = req.text
    soup = bs(html, 'html.parser')
    my_pages = soup.select(
        '#paging > span > a'
    )
    LastPage = my_pages[-1].get('href')
    if LastPage == None:
        break
    GetLastPage = LastPage
print(GetLastPage)



data = {}
#마지막 페이지까지 순회하면서 리스트 가져오기
for i in range(1, int(GetLastPage[-1])+1):
    req = requests.get(stemURL + GetLastPage[:-1] + str(i) , headers=headers)
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.select(
    '#searchList > ol > li > a'
   )
    dates = soup.select(
        '#searchList > ol > li > span.date'
    )
    for title, date in zip(my_titles, dates):
        data[title.text] = title.get('href')
        print('{}  {}'.format(date.text ,title.text))

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
   json.dump(data, json_file)
