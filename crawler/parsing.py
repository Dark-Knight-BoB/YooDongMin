import re

emailPat=re.compile('[^@]+@[^@]+\.[^@]+')
telPat = re.compile('(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
ipPat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
bitcoinPat =re.compile('[13][a-km-zA-HJ-NP-Z0-9]{26,33}')
moneroPat = re.compile('4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}')
