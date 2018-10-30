from bs4 import BeautifulSoup as bs
import requests
import requests.exceptions
from collections import deque
import re

stemURL='http://highkorea5ou4wcy.onion'

html = "null"
emails = set()
domain = set()

req = requests.get(stemURL)
html =req.text


def parser(html):
	new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",req.text, re.I))
	new_domain = set(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',req.text,re.I))
	emails.update(new_emails)
	domain.update(new_domain)


parser(html)
print(html)
print("======================================================================")
print(emails)
print("======================================================================")
print(domain)
print("======================================================================")






