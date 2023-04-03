import requests
import re
import os

from bs4 import BeautifulSoup

def requestWeb(website):
    request = requests.get(website, headers={"User-Agent": "Mozilla/5.0"})  # Requests access
    return BeautifulSoup(request.text, 'html.parser')

# Gets the links
def filterWeb(soup):
    spoonedDiv = soup.find_all(["ul", "h3"], attrs={'class': None})
    spoonedDiv = soup.find_all(["a", "h3"], attrs={'class': None})
    return spoonedDiv

# Gets the information from the website.
def scrapeResults(soup):
    # Gets the description
    desc = soup.find_all("p", attrs={'class': None}, limit=2)
    desc = str(desc[1].text)

    # Gets the attibutes.
    attrList = []
    attrs = soup.select('table > tbody > tr')
    
    # Cleans and adds attributes to a list.
    for attr in attrs:
        buildStr = str(attr.select("td > code")).replace("<code>", "").replace("</code>", "").replace("[", "").replace("]", "").split(",")[0]
        attrList.append(buildStr)

    return desc, attrList

def buildSnippet(soup, name, desc, attrList):
    # Build the skeleton... (SANS UNDERTALE???)
    build = [f'"{name}": {{']
    build.append(f'\t"prefix": "{name}",')
    build.append('\t"scope": "json",')
    build.append('\t"body": [')

    for attr in attrList: # Attributes
        buildStr = ""
        buildStr += f'\t\t"{attr}": ""'
        if attr != attrList[len(attrList) - 1]:
            buildStr += ","
        build.append(buildStr)

    build.append('\t],')
    build.append(f'\t"description": "{desc}"')
    build.append("}")

    for ele in build: print(ele)

# "placeholder": {
#     "prefix": "placeholder",
#     "scope": "json",
#     "body": [
#         "placeholder",
#     ],
#     "description": "(Power Type)"
# }


# Main program (woo...)
mainWeb = "https://origins.readthedocs.io/en/latest/types/power_types/"

for tag in filterWeb(requestWeb(mainWeb)):
    # filters the important information
    reg = re.compile('<a.*href="(?!\\.)(?!http)([a-zA-Z].*)">(.*)</a>|<h3.*>(.*)</h3>').search(str(tag))
    
    if reg:
        if reg.group(1) and reg.group(2):
            # Scrape web if not an h3
            newWeb = requestWeb(f"{mainWeb}{reg.group(1)}")
            desc, attrs = scrapeResults(newWeb) # Gets the data we want.
            buildSnippet(newWeb, reg.group(1)[:-1], desc, attrs) # Builds the snippet.
            break # leave this here for now, we dont want to clog the terminal.