#!/usr/bin/python
import os, sys
from lxml import html
import requests
from pynma import PyNMA


def getXpathText(element, xpathPattern):
    """
    Get text from a HTML element based on an Xpath and convert to utf-8 encoding
    Return an emptyh string of the xpath can not be found 
    """
    result = element.xpath(xpathPattern)
    if result:
        return result[0].encode('utf-8')
    else:
        return ""

def enableUTF8():
    """Enables UTF-8 Encoding"""
    reload(sys)  
    sys.setdefaultencoding('Cp1252')

def setupNMA(keyFile):
    """Return and instance of PyNMA with the NMA api key loaded"""
    p = PyNMA()

    nmaKey = open(keyFile, 'r').readline().strip()
    p.addkey(nmaKey)

    return p

def recordEntry(notifier, file, title, description, link):
    print title + "\n" + description + "\n" + link + "\n\n"
    file.write(title + "\n")
    print notifier.push("MMA Fighting Update", title, description, link, batch_mode=False)


# Constants
URL = 'http://www.mmafighting.com/latest-news'

BODYS_XPATH = '//div[contains(@class, "m-block__body")]/header/..'
TITLE_XPATH = 'header/h3/a/text()'
DESCRIPTION_XPATH = 'p/text()'
HREF_XPATH = 'header/h3/a/@href'

#TODO These two constant may want to be passed in
NMA_KEY_FILE = "api-key.txt"
HEADLINE_FILE = "mma-fighting.txt"

def main():
    # Enable UTF-8 encoding
    enableUTF8()

    # Setup nma notifications
    nma = setupNMA(NMA_KEY_FILE)

    # Get the page
    page = requests.get(URL)

    # Form the tree to parse
    tree = html.fromstring(page.content)

    # Get the outer summary bodies in reverse order 
    bodies = tree.xpath(BODYS_XPATH)[::-1]

    # Extract the title, description and link from each body and store in tuples in that order
    contentTuples = [(getXpathText(b,TITLE_XPATH), getXpathText(b,DESCRIPTION_XPATH), getXpathText(b,HREF_XPATH)) for b in bodies]

    # Open the headline file to read and append to
    with open(HEADLINE_FILE, "r+") as headlineFile:
        # Read each line of the file to check for repeat occurrences
        lines = headlineFile.readlines()

        # Go through each headline extracted and check if the headline has already been recorded
        for headline in contentTuples:
            if headline[0]+"\n" not in lines:
                recordEntry(nma, headlineFile, *headline)

if __name__ == "__main__":
    main()
