import requests
from bs4 import BeautifulSoup as bs
stemURL='http://highkorea5ou4wcy.onion'
req = requests.get(stemURL)

html = req.text

status = req.status_code

soup = bs(html, 'html.parser')

mainCategory = soup.find_all("a", {"class":"forumtitle"})
for category in mainCategory:
    print("Forum : {}".format(category.text))
    forumUrl= category.get('href')
    req = requests.get(stemURL+forumUrl.strip('.'))
    soup = bs(req.text,'html.parser')
    titles = soup.find_all("a", {"class":"topictitle"})
    for title in titles:
        print("title : {}".format(title.text))
        titleURL = title.get('href')
        req = requests.get(stemURL+titleURL.strip('.'))
        soup = bs(req.text,'html.parser')
        contents = soup.find_all("div", {"class": "content"})
        for content in contents:
            print(content.get_text())
        print("-------------------------------------------------------------------")
    print("======================================================================================================================================================")