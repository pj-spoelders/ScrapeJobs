import datetime
import json
import locale
import random
from typing import Optional, Any, List

import requests
import urllib.request
import time
from bs4 import BeautifulSoup, Tag, ResultSet
import re
import html5lib
from selenium import webdriver
import dateparser

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
    assert len(infoElements) > 0 and len(
        infoElements) <= expectedResultsPerPage, "Something's wrong with the soup, expected more than 0 and no more than 15 elements"
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
    def __init__(self, title, href, company, location, jobtype,createdon, updatedon):
        self.Href = href
        self.Title = title
        self.Company = company
        self.Location = location
        self.JobType = jobtype
        self.CreatedOn = createdon
        self.UpdatedOn = updatedon

    Title: str
    Href: str
    Company: str
    Location: str
    JobType: str
    CreatedOn: datetime.date
    UpdatedOn: datetime.date

# https://realpython.com/python-json/#python-supports-json-natively
class CustomJobInfoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JobInfo):
            updatedOnStr :str
            if o.UpdatedOn is None:
                updatedOnStr = ""
            else:
                updatedOnStr = o.UpdatedOn.strftime("%d/%m/%Y")
            return (o.Href,o.Title,o.Company,o.Location,o.JobType,o.CreatedOn.strftime("%d/%m/%Y"),updatedOnStr)
        return super().default(o)

def AddJobsFromInfoElements(infoElements: ResultSet):
    jobsList: List[JobInfo] = []

    info: Tag
    for info in infoElements:
        jobsList.append(ParseInfo(info))

    return jobsList

# expects '9 juli 2018' or similar
def DutchDateStrToDate(dds: str):
    # just use smth like babel instead of messing about with locale
    # see this: https://stackoverflow.com/questions/52373931/options-for-converting-between-localized-strings-and-datetime-objects
    # we're going to use dateparser https://github.com/scrapinghub/dateparser
    dt = dateparser.parse(dds, languages=['nl'])
    return dt

def ParseInfo(info):
    infoTag: Tag = info.contents[1]
    Title = infoTag.find("div", {"class": "slat-title"}).text
    locationTag: Tag = infoTag.find(class_="location")
    locationTagStrongTags = locationTag.find_all("strong")
    Company = locationTagStrongTags[0].text
    Location = locationTagStrongTags[1].text
    jobTypeTag: Tag = infoTag.find(class_="job-type")
    jobTypeSpanTags: ResultSet = jobTypeTag.find_all("span")
    JobType = jobTypeSpanTags[0].text
    CreatedOn = DutchDateStrToDate(jobTypeSpanTags[1].text[16:])  # slicing
    if len(jobTypeSpanTags) == 3:
        UpdatedOn = DutchDateStrToDate(jobTypeSpanTags[2].text[19:])
    else:
        UpdatedOn = None
    Href = info.attrs["href"]

    return JobInfo(Title, Href, Company, Location,JobType, CreatedOn, UpdatedOn)



nrOfResults = GetNrOfResultsFromPage()
nrOfResultPerPage = 15
nrOfOtherPagesToScrape = nrOfResults // nrOfResultPerPage - 1

page1InfoElements = GetInfoElementsFromPageSoup(page1Soup, nrOfResultPerPage)

jobsList: List[JobInfo] = []

jobsList += AddJobsFromInfoElements(page1InfoElements)

with open("data_file.json", "w") as write_file:
    json.dump(jobsList,fp=write_file,cls=CustomJobInfoEncoder)
    #jsonStr = json.dumps(jobsList, cls=CustomJobInfoEncoder)


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
