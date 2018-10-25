import requests, json
from bs4 import BeautifulSoup as bs
#freshonion='http://zlal32teyptf4tvi.onion/language/ko/json'
freshonion='http://zlal32teyptf4tvi.onion/json/all'
req = requests.get(freshonion)

html = req.text

status = req.status_code
#print(html)
datas = json.loads(html)

for data in datas:
    print("===================================================")
    title = '제목 없음'
    if data['title'] != "":
        title = data['title']
    print("{} : {}({})".format(data['hostname'], title, data['is_up']))