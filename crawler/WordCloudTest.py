#-*- coding:utf-8 -*-
from konlpy.tag import Hannanum
from konlpy.utils import pprint
from collections import Counter
import requests
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.font_manager as fm
from matplotlib import rc
from wordcloud import WordCloud
print('# 설정되어있는 폰트 사이즈')
print (plt.rcParams['font.size'] )
print('# 설정되어있는 폰트 글꼴')
print (plt.rcParams['font.family'] )
path = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
#fontprop = fm.FontProperties(fname=path, size=18)
font_name = fm.FontProperties(fname=path).get_name()
f = open('/home/kyw/highkorea/highkorea.txt')
text = f.read()
wordcloud = WordCloud().generate(text)
wordcloud.words_
plt.figure(figsize=(12,12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
f.close()

'''
print ('버전: ', mpl.__version__)
print ('설치 위치: ', mpl.__file__)
print ('설정 위치: ', mpl.get_configdir())
print ('캐시 위치: ', mpl.get_cachedir())
print ('설정 파일 위치: ', mpl.matplotlib_fname())
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
print([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])
# ttf 폰트 전체개수
print(len(font_list))
'''
