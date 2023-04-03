import requests
import re
import os

from bs4 import BeautifulSoup

def requestWeb(website):
    request = requests.get(website, headers={"User-Agent": "Mozilla/5.0"})  # Requests access
    return BeautifulSoup(request.text, 'html.parser')

# Gets the links
def filterWeb(htmlSpoon):
    spoonedDiv = htmlSpoon.find_all(["ul", "h3"], attrs={'class': None})
    spoonedDiv = htmlSpoon.find_all(["a", "h3"], attrs={'class': None})
    return spoonedDiv

# Gets the information from the website.
def scrapeResults(htmlSpoon):
    # Gets the description
    desc = htmlSpoon.find_all("p", attrs={'class': None}, limit=2)
    print(str(desc[1].text)+"\n") 

    # Gets the attibutes.
    attrList = []
    attrs = htmlSpoon.select('table > tbody > tr')
    
    # Cleans and adds attributes to a list.
    for attr in attrs:
        buildStr = str(attr.select("td > code")).replace("<code>", "").replace("</code>", "").replace("[", "").replace("]", "").split(",")[0]
        attrList.append(buildStr)
        
    print(attrList)

# Main program (recursivity, woo...)
mainWeb = "https://origins.readthedocs.io/en/latest/types/power_types/"

for tag in filterWeb(requestWeb(mainWeb)):
    # filters the important information
    reg = re.compile('<a.*href="(?!\\.)(?!http)([a-zA-Z].*)">(.*)</a>|<h3.*>(.*)</h3>').search(str(tag))
    
    if reg:
        if reg.group(1) and reg.group(2):
            # Scrape web if not an h3
            print(reg.group(1))
            scrapeResults(requestWeb(f"{mainWeb}{reg.group(1)}"))
            break # leave this here for now, we dont want to clog the terminal.


# "placeholder" : {
#     "prefix": "placeholder",
#     "scope": "json",
#     "body": [
#         "placeholder",
#     ],
#     "description": "(Power Type)"
# }