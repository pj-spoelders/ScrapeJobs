import random
from typing import Optional, Any

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import html5lib
from selenium import webdriver


def GetPageHtmlViaSelenium(driver, url):
    # get web page
    driver.get(url)
    # execute script to scroll down the page
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep
    time.sleep(1)  # wait for content to load
    print("I slept")
    html = driver.page_source
    return html

def GetInfoElementsFromPageSoup(soup):
    infoElements = soup.find_all("div", {"class": "-info"})
    print("searched soup")

print("Start scraping")
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
# https://pythonspot.com/selenium-phantomjs/

url = 'https://www.vdab.be/vindeenjob/vacatures?locatie=8630%20veurne&afstand=10&sort=standaard&jobdomein=JOBCAT10'
driver = webdriver.PhantomJS()

page1Html = GetPageHtmlViaSelenium(driver, url)
page1Soup = BeautifulSoup(page1Html)

nrOfResultsElement = page1Soup.find("strong")  #  {"id": "vej-totaal-jobs-gevonden"})
nrOfResultsStr = nrOfResultsElement.text
nrOfResults = int( nrOfResultsStr)
nrOfResultPerPage = 15
nrOfOtherPagesToCheck = nrOfResults / nrOfResultPerPage - 1
time.sleep(1)

GetInfoElementsFromPageSoup(page1Soup)



detailUrl = 'https://www.vdab.be/vindeenjob/vacatures/59880135/applicatiebeheerder-met-feeling-voor-testing-en-ervaring-in-een-labo-omgeving'
response = requests.get(detailUrl)

print(response.text)

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

# print(spans)
# print(nrOfJobsSpan)

print("end of program")
# print(soup.findAll('a'))
