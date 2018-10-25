import requests
from bs4 import BeautifulSoup as bs
hiddenwiki='https://thehiddenwiki.org/'
req = requests.get(hiddenwiki)

html = req.text

status = req.status_code

soup = bs(html, 'html.parser')

div = soup.select(
    '#post-2 > div.entry'
)

atags = div[0].findAll('a')
for i, a in enumerate(atags):
    print("Try %d" %i)
    url = a.get('href')
    try:
        req = requests.get(url)
        if req.status_code == 200:
            print("{} : {}".format(url, req.ok))
    except requests.exceptions.RequestException as e:
        print("{} : {}".format(url, "Cannot Connect!"))
        pass

#http://kohdwk5fr42cs3rg.onion/index.php?title=%EB%8C%80%EB%AC%B8
#http://hwikis25cffertqe.onion/index.php?title=%EB%8B%A4%ED%81%AC%EB%84%BD_%EC%8B%B8%EC%9D%B4%ED%8A%B8
#http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page
