from bs4 import BeautifulSoup as bs
import requests
import requests.exceptions
from urlparse import urlsplit
from collections import deque
import re

 
def EmailParsing(siteURL):
	new_urls = deque([siteURL])						# a queue of urls to be crawled
	processed_urls = set() 							# a set of urls that we have already crawled
	emails = set()									# a set of crawled emails

# process urls one by one until we exhaust the queue
	while len(new_urls):

    # move next url from the queue to the set of processed urls
		url = new_urls.popleft()
		processed_urls.add(url)

    # extract base url to resolve relative links
		parts = urlsplit(url)
		base_url = "{0.scheme}://{0.netloc}".format(parts)
		path = url[:url.rfind('/')+1] if '/' in parts.path else url
		print("Processing %s" % url)
		try:
			response = requests.get(url)
		except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
			continue
    # extract all email addresses and add them into the resulting set
		new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
		emails.update(new_emails) 
		print(emails)
    # create a beutiful soup for the html document
		soup = bs(response.text,'html.parser')

    # find and process all the anchors in the document
		for anchor in soup.find_all("a"):
        # extract link url from the anchor
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links
			if link.startswith('/'):
				link = base_url + link
			elif not link.startswith('http'):
				link = path + link
        # add the new url to the queue if it was not enqueued nor processed yet
			if not link in new_urls and not link in processed_urls:
				new_urls.append(link)

keyword = [ "northkorea" , "drug"]

for search in keyword: #keyword search
	print("Searching : "+search)
	page = 1
	req = requests.get("http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page=1")
	html = req.text
	soup = bs(html,'html.parser')
	content = soup.find_all('div',{'class':'ruler'})
        if(content):
            print("PAGE : 1")
            domain = "http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page="+str(page)
            EmailParsing(domain)
        else:
            while page < 20: #page loop
                print("PAGE : "+ str(page) )
                domain = "http://zlal32teyptf4tvi.onion/?search="+search+"&rep=n%2Fa&page="+str(page)
                EmailParsing(domain)
                page += 1
	
				
