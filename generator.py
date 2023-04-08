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
def scrapeResults(soup, name):
    # Gets the description
    desc = soup.find_all("p", attrs={'class': None}, limit=2)
    desc = str(desc[1].text)

    # Check if the power has at least one field.
    if "<p><em>None.</em></p>" in str(soup) or not soup.find("table"):
        return desc, [None], [None], name

    # Gets the attibutes.
    attrList = []
    valuesList = []
    attrs = soup.select('table > tbody > tr')
    
    # Cleans and adds attributes to a list.
    for attr in attrs:
        buildStr = str(attr.select("td > code")).replace("<code>", "").replace("</code>", "").replace("[", "").replace("]", "").split(",")[0]
        attrList.append(buildStr)

    # Gets the (raw) values.
    values = soup.find("table")
    values = values.select('tbody > tr > td > a')
    values = [x for x in values if not "../../../" in str(x)]
    for value in values:
        valuesList.append(value.contents[0]) 

    return desc, attrList, valuesList, name

# Builds a snippet. Technically there is a bug when a value has two "<a>" tags, but I just don't care and i'll fix it manually.
def buildSnippet(soup, name, desc, attrList, valuesList):
    # Build the skeleton... (SANS UNDERTALE???)
    build = [f'"{name}": {{']
    build.append(f'\t"prefix": "{name}",')
    build.append('\t"scope": "json",')
    build.append('\t"body": [')

    # Adds the attributes via a for loop.
    i = 0
    for attr in attrList:
        buildStr = ""
        
        if i >= len(valuesList): break

        if attr is None: buildStr += f'\t\t"\\\"type\\\": '
        else: buildStr += f'\t\t\"\\\"{attr}\\\": '

        # Type of the value
        match valuesList[i]:
            case "Boolean":
                buildStr += 'true'
            case "Float":
                buildStr += '1.0'
            case "Integer":
                buildStr += '1'
            case "String" | "Identifier":
                buildStr += '\\\"\\\"'
            case "Array":
                buildStr += '[]'
            case None:
                buildStr += f'\\\"origins:{name}\\\"'
            case _:
                buildStr += '{}'

        # Should a comma be added?
        if attr != attrList[len(attrList) - 1]:
            buildStr += ","

        buildStr += "\","
        build.append(buildStr)
        i += 1

    build.append('\t],')
    build.append(f'\t"description": "{desc}"')
    build.append("},")
    return build

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
if not os.path.exists("./snippets/powers"): os.mkdir("./snippets/powers")

for tag in filterWeb(requestWeb(mainWeb)):
    # Filters the important information
    reg = re.compile('<a.*href="(?!\\.)(?!http)([a-zA-Z].*)">(.*)</a>|<h3.*>(.*)</h3>').search(str(tag))

    if reg:
        if reg.group(3):
            # Initializes a snippet file.
            file = open(f"./snippets/powers/{reg.group(3).lower().replace(' ', '-')}.code-snippets", "a")
            file.write("{")

        elif reg.group(1) and reg.group(2):
            # Scrape web if not an h3.
            newWeb = requestWeb(f"{mainWeb}{reg.group(1)}")
            desc, attrs, values, name = scrapeResults(newWeb, reg.group(1)[:-1]) # Gets the data we want.
            snippet = buildSnippet(newWeb, name, desc, attrs, values) # Builds the snippet.
            
            # Updates the file.
            for ele in snippet: file.write(f"{ele}")
file.write("}")