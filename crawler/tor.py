import requests
with requests.session() as s:
    s.proxies = {}
    s.proxies['http'] = 'socks5h://localhost:9050'
    s.proxies['https'] = 'socks5h://localhost:9050'
    # r = s.get('http://httpbin.org/ip')
    # print(r.text)
