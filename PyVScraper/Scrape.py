from typing import Optional, Any

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import html5lib
from selenium import webdriver

print("Hello")
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
# https://pythonspot.com/selenium-phantomjs/

url = 'https://www.vdab.be/vindeenjob/vacatures?locatie=8630%20veurne&afstand=10&sort=standaard&jobdomein=JOBCAT10'
driver = webdriver.PhantomJS()
# get web page
driver.get(url)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep
time.sleep(1)
print("I slept")
html = driver.page_source
print(html)

# response = requests.get(url)
# print(response)
#
# soup = BeautifulSoup(response.text, 'html5lib')
#
# divResults = soup.find_all('div')
#
# regexJobsGevonden = re.compile("Jobs gevonden")
# spans = soup.find_all('span')
# nrOfJobsSpan = soup.find('span', text=regexJobsGevonden)
# print(divResults)

#print(spans)
#print(nrOfJobsSpan)

print("end of program")
# print(soup.findAll('a'))
