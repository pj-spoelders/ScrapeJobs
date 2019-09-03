from typing import Optional, Any

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import html5lib

print("Hello")
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
url = 'https://www.vdab.be/vindeenjob/vacatures?locatie=8630%20veurne&afstand=10&sort=standaard&jobdomein=JOBCAT10'
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text)

aResults = soup.find_all('a')
strongFound = soup.find_all('strong')
strongNumberFound = soup.find_all({"class": "vej-totaal-jobs-gevonden"})
results = soup.find_all('div')
divResults = soup.find_all('div', {"id":"results"})

spans = soup.find_all('span')
nrOfJobsSpan = soup.find('span', text=regexJobsGevonden)
print(divResults)

#print(spans)
#print(nrOfJobsSpan)

print("end of program")
# print(soup.findAll('a'))
