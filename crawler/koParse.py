import matplotlib.pyplot as plt
from wordcloud import WordCloud
#from PIL import Image
#from wordcloud import STOPWORDS
import nltk
from konlpy.tag import Mecab
import numpy as np
mecab = Mecab()
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
f = open('/home/kyw/highkorea/highkorea.txt', encoding = 'utf-8')
text = f.read()
tokens_ko = mecab.nouns(text)
stop_words = ['제','수','내','이','저','그','거','게','걸','때','나','우리','때문','것','뿐','면','등','일','년','글','분','말']
tokens_ko = [each_word for each_word in tokens_ko if each_word not in stop_words]
ko = nltk.Text(tokens_ko, name='highkorea')
data = ko.vocab().most_common(30)
tmp_data = dict(data)
wordcloud = WordCloud(font_path=path, relative_scaling=0.2, background_color='white', width=800, height=800).generate_from_frequencies(tmp_data)
plt.figure(figsize=(12,12))
print(type(wordcloud))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
f.close()
