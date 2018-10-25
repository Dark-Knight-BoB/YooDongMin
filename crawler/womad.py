from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup as bs

display = Display(visible=1, size=(800, 600))
display.start()
driver = webdriver.Chrome()
driver.get('https://womad.life/b/%EC%9B%8C%EB%85%90%EA%B8%80/1?id=606427')
driver.implicitly_wait(6)

