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
    if "<p><em>None.</em></p>" in str(soup):
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
        # Fiddle with this!!!!! example: conditioned_attribute
        # Attributed Attribute Modifier 0
        # Array 1 <------ BAD!!! (array)
        # Attributed Attribute Modifiers 2
        # Integer 3

    return desc, attrList, valuesList, name

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
        
        if attr is None: buildStr += f'\t\t"type": '
        else: buildStr += f'\t\t"{attr}": '

        # Type of the value
        print(valuesList[i], i)
        match valuesList[i]:
            case "Boolean":
                buildStr += 'true'
            case "Float":
                buildStr += '1.0'
            case "Integer":
                buildStr += '1'
            case "String" | "Identifier":
                buildStr += '""'
            case None:
                buildStr += f'"origins:{name}"'
            case _:
                buildStr += '{}'

        # Should a comma be added?
        if attr != attrList[len(attrList) - 1]:
            buildStr += ","

        build.append(buildStr)
        i += 1

    build.append('\t],')
    build.append(f'\t"description": "{desc}"')
    build.append("}")

    # Prints the mess that this is.
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
    # future me im sorry but you must fix this
    # im leaving a comment big enough
    # so you cannot miss it when
    # you start debugging
    # haha nerd get fucked
    if reg:
        if reg.group(3):
            file = open(f"./snippets/powers/{reg.group(3).replace(' ', '-')}.code-snippets", "a")
        elif reg.group(1) and reg.group(2):
            # Scrape web if not an h3
            newWeb = requestWeb(f"https://origins.readthedocs.io/en/latest/types/power_types/attribute/") # {mainWeb}{reg.group(1)}
            desc, attrs, values, name = scrapeResults(newWeb, reg.group(1)[:-1]) # Gets the data we want.
            buildSnippet(newWeb, name, desc, attrs, values) # Builds the snippet.
            break # leave this here for now, we dont want to clog the terminal.