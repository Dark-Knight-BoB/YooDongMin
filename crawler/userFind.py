import requests
from multiprocessing import Pool
from itertools import repeat
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re, time
def find(url, user):
    with requests.session() as s:

        retries = Retry(total=5,
                        backoff_factor=0.5,
                        )
        s.mount('http://', HTTPAdapter(max_retries=retries))
        URL = url.format(user)
        try:
            req = s.get(URL)
            if req.status_code == 200:
                if DC.replace('{}','') in URL:
                    if re.compile('http://gallog.dcinside.com/_error/rest').search(req.text):
                        return None
                return URL
        except Exception as e:
            print(URL, "\n", e)

if __name__ == '__main__':
    google = 'https://www.google.co.kr/search?q={}'
    twitter = 'https://twitter.com/{}'
    instagram = 'https://www.instagram.com/{}'
    naverblog = 'https://blog.naver.com/{}'
    daumblog = 'http://blog.daum.net/{}'
    youtube = 'https://www.youtube.com/user/{}'
    tistory = 'http://{}.tistory.com/'
    ilbe = 'http://www.ilbe.com/index.php?mid=ilbe&search_target=nick_name&search_keyword={}'
    ilbeContent = 'http://www.ilbe.com/?act=IS&where=document&is_keyword={}'
    DC = 'http://gallog.dcinside.com/{}'
    tumblr = 'https://{}.tumblr.com/'
    uid = 'h33333r0'

    sites = [google,twitter,instagram,naverblog,daumblog,youtube,tistory,ilbe,ilbeContent,DC,tumblr]
    pool = Pool(processes=4)
    start_time = time.time()
    results = pool.starmap(find, zip(sites, repeat(uid)))
    print("--- %s seconds ---" % (time.time() - start_time))
    print(results)
