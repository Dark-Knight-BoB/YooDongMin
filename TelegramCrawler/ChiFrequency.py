import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import nltk
from snownlp import SnowNLP
import json
import operator
import numpy as np
import operator

tokens_chi = []
tokens_err = []
message_count=0
with open('/home/kyw/json_datas/tele_2018_10_03_16:38.json') as f:
    data = json.load(f)
    message_count=len(data)
    for message in data:
        try:
            s = SnowNLP(message['text'])
            tokens_chi.extend(s.words)
        except TypeError:
            words = [dic['text'] for dic in message['text'] if type(dic) == dict]
            for word in words:
                s = SnowNLP(word)
                tokens_err.extend(s.words)

tokens_chi.extend(tokens_err)

data = {}
with open('/home/kyw/Desktop/mushroom.txt') as rf:
    for line in rf.readlines():
        data[line.strip('\n')] = tokens_chi.count(line.strip('\n'))

'''
to = nltk.Text(tokens_chi, name='Telegram')
data = to.vocab().most_common(100)
print(data)
'''


sorted_data = sorted(data.items(), key=operator.itemgetter(1))
words = [word[0] for word in sorted_data][-20:]
frequency = [(word[1]/message_count)*100 for word in sorted_data][-20:]
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ypos = np.arange(20)
rects = plt.barh(ypos, frequency, align='center', height=0.5)
plt.yticks(ypos, words)
for i, rect in enumerate(rects):
    ax.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(frequency[i]) + '%', va='center')
plt.xlabel('언급 빈도(비율)')
plt.show()