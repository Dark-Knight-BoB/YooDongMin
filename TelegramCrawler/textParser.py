import json
from workspace.crawler import Crawler
from collections import OrderedDict
telegramchats = []

with open('/home/kyw/Downloads/Telegram Desktop/2018_10_03_16:38/result.json') as f:
    data = json.load(f)
    messages = data['chats']['list'][0]['messages']
    for i, message in enumerate(messages):
        if 'from' in message.keys() and message['text'] != '':
            chat = OrderedDict()
            chat['count'], chat['id'], chat['data'], chat['from'] , chat['text'] = i, message['id'], message['date'], message['from'], message['text']
            telegramchats.append(chat)
            #print("==================================================================")
            #print('id : {}\nDate : {}\nActor : {}\nText : {}'.format(message['id'],message['date'],message['from'], message['text']))
        else:
            continue

    Crawler.mkjson('/home/kyw/json_datas/', telegramchats, 'tele_2018_10_03_16:38.json')
