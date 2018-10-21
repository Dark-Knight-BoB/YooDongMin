import agoraNewPage as ag
import re
import time
import Crawler as cr
from collections import OrderedDict
from multiprocessing import Pool

if __name__ == '__main__':
    start_time = time.time()
    lastpage = int(ag.get_link())
    data = ag.agoraStemCrawler()
    pool = Pool(processes=4)
    datas = pool.map(ag.agoraMultiCrawler, range(lastpage+1))
    datas.append(data)
    cr.mkjson(datas, '/home/kyw/json_datas/agora', 'agora_all.json')
