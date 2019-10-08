import datetime
import json
import random
from typing import Optional, Any, List

import requests
import urllib.request
import time
from bs4 import BeautifulSoup, Tag, ResultSet
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
    time.sleep(10)  # wait for content to load, since the VDAB site is slow as molasses, give it a ton of time ..
    print("I slept")
    html = driver.page_source
    return html


def GetInfoElementsFromPageSoup(soup, expectedResultsPerPage):
    infoElements = soup.find_all("a", {"class": "slat-link"})
    assert len(infoElements) > 0 and len(infoElements) <= expectedResultsPerPage, "Something's wrong with the soup, expected more than 0 and no more than 15 elements"
    print("searched soup")
    return infoElements


print("Start scraping")
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
# https://pythonspot.com/selenium-phantomjs/

url = 'https://www.vdab.be/vindeenjob/vacatures?locatie=8630%20veurne&afstand=10&sort=standaard&jobdomein=JOBCAT10'
driver = webdriver.PhantomJS()

page1Html = GetPageHtmlViaSelenium(driver, url)
page1Soup = BeautifulSoup(page1Html)


def GetNrOfResultsFromPage():
    nrOfResultsElement = page1Soup.find("strong",
                                        {"id": "vej-totaal-jobs-gevonden"})  # {"id": "vej-totaal-jobs-gevonden"})
    assert nrOfResultsElement is not None, "Page API call for content not executed yet."
    nrOfResultsStr = nrOfResultsElement.text
    nrOfResults = int(nrOfResultsStr)
    return nrOfResults


class JobInfo:
    def __init__(self, title, href, company, location, createdon, updatedon):
        self.Href = href
        self.Title = title
        self.Company = company
        self.Location = location
        self.CreatedOn = createdon
        self.UpdatedOn = updatedon

    Title: str
    Href: str
    Company: str
    Location: str
    JobType: str
    CreatedOn: datetime.date
    UpdatedOn: datetime.date


def AddJobsFromInfoElements(infoElements: ResultSet):
    jobsList: List[JobInfo] = []

    info: Tag
    for info in infoElements:
        infoTag : Tag = info.contents[1]
        Title = infoTag.find("div", {"class": "slat-title"}).text

        locationTag : Tag = infoTag.find(class_="location")
        locationTagStrongTags = locationTag.find_all("strong")
        Company = locationTagStrongTags[0].text
        Location =  locationTagStrongTags[1].text

        jobTypeTag: Tag = infoTag.find(class_="job-type")
        jobTypeSpanTags : ResultSet = jobTypeTag.find_all("span")
        JobType = jobTypeSpanTags[0].text
        CreatedOn = jobTypeSpanTags[1].text
        if len(jobTypeSpanTags) == 3:
            ChangedOn = jobTypeSpanTags[2].text
        Href = info.attrs["href"]


        jobsList.append(JobInfo(infoElements.attrs))

    return jobsList


nrOfResults = GetNrOfResultsFromPage()
nrOfResultPerPage = 15
nrOfOtherPagesToScrape = nrOfResults // nrOfResultPerPage - 1

page1InfoElements = GetInfoElementsFromPageSoup(page1Soup, nrOfResultPerPage)

jobsList: List[JobInfo] = []

jobsList += AddJobsFromInfoElements(page1InfoElements)

jsonStr = json.dumps(jobsList)

# detailUrl = 'https://www.vdab.be/vindeenjob/vacatures/59880135/applicatiebeheerder-met-feeling-voor-testing-en-ervaring-in-een-labo-omgeving'
# response = requests.get(detailUrl)
# print(response.text)

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
