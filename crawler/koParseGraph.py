import matplotlib.pyplot as plt
from wordcloud import WordCloud
#from wordcloud import STOPWORDS
import nltk
from konlpy.tag import Mecab
import numpy as np
mecab = Mecab()
wordcloud=WordCloud()
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
f = open('/home/kyw/highkorea/highkorea.txt', encoding = 'utf-8')
text = f.read()
tokens_ko = mecab.nouns(text)
print(tokens_ko)
stop_words = ['제','수','내','이','저','그','거','게','걸','때','나','우리','때문','것','뿐','면','등','일','년','글','분','말']
tokens_ko = [each_word for each_word in tokens_ko if each_word not in stop_words]
ko = nltk.Text(tokens_ko, name='highkorea')
data = ko.vocab().most_common(10)
print(data)
tmp_data = dict(data)
print(tmp_data)
words = [word[0] for word in tmp_data.items()]
frequency = [word[1] for word in tmp_data.items()]
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ypos = np.arange(10)
rects = plt.barh(ypos, frequency, align='center', height=0.5)
plt.yticks(ypos, words)
plt.xlabel('빈도')
plt.show()
f.close()
