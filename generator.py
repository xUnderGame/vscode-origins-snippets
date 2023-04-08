import requests
import re
import os

from bs4 import BeautifulSoup

def requestWeb(website):
    request = requests.get(website, headers={"User-Agent": "Mozilla/5.0"})
    return BeautifulSoup(request.text, 'html.parser')

# Gets the links
def filterWeb(soup):
    spoonedDiv = soup.find_all(["ul", "h3"], attrs={'class': None})
    spoonedDiv = soup.find_all(["li", "h3"], attrs={'class': None}) # Change "li" to "a" to get powers.
    return spoonedDiv

# Gets the information from the website.
def scrapeResults(soup, name):
    # Gets the description
    desc = soup.find_all("p", attrs={'class': None}, limit=2)
    desc = str(desc[1].text).replace("\"", "\\\"")

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
    values = values.select('tbody > tr > td:has(a)')
    values = [x for x in values if not "../../../" in str(x)]

    for value in values:
        try:
            valuesList.append(value.contents[0].contents[0])
        except AttributeError:
            print(f"{name} can't be fetched correctly.") # Or maybe it can and im just dum. (most of the time its a false-positive)
            desc, [None], [None], name

    return desc, attrList, valuesList, name

# Builds a snippet.
def buildSnippet(soup, name, desc, attrList, valuesList):
    # Build the skeleton... (SANS UNDERTALE???)
    build = [f'"{name}": {{'] # remove {}
    build.append(f'\t"prefix": "{entryType}{name}",')
    build.append('\t"scope": "json",')
    build.append('\t"body": [')
    build.append(f'\t\t"\\\"type\\\": \\\"origins:{name}\\\"",')

    # Adds the attributes via a for loop.
    i = 0
    for attr in attrList:
        buildStr = ""
        
        if attr is None: 
            build[-1].replace(",", "")
            break
        if i >= len(valuesList): break

        buildStr += f'\t\t\"\\\"{attr}\\\": '

        # Type of the value
        match valuesList[i]:
            case "Boolean":
                buildStr += f'${{{i + 1}|true,false|}}'
            case "Float":
                buildStr += f'${{{i + 1}:1.0}}'
            case "Integer":
                buildStr += f'${{{i + 1}:1}}'
            case "String" | "Identifier":
                buildStr += f'\\\"${{{i + 1}}}\\\"'
            case "Array":
                buildStr += f'[${{{i + 1}}}]'
            case _:
                buildStr += f'{{${i + 1}}}'

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
mainWeb = "https://origins.readthedocs.io/en/latest/types/entity_condition_types/"
folder = "./snippets/conditions/entity/"
entryType = "entity:" # change if you need it (default use is "", nothing)
file = None
if not os.path.exists(folder): os.mkdir(folder)

for tag in filterWeb(requestWeb(mainWeb)):
    # Filters the important information
    reg = re.compile('<a.*href="(?!\\.)(?!http)([a-zA-Z].*)">(.*)</a>|<h3.*>(.*)</h3>').search(str(tag))

    if reg:
        if reg.group(3):
            # Initializes a snippet file.
            if file: file.write("}")
            file = open(f"{folder}{reg.group(3).lower().replace(' ', '-')}.code-snippets", "a")
            file.write("{")

        elif reg.group(1) and reg.group(2):
            # Scrape web if not an h3.
            newWeb = requestWeb(f"{mainWeb}{reg.group(1)}")
            desc, attrs, values, name = scrapeResults(newWeb, reg.group(1)[:-1]) # Gets the data we want.
            snippet = buildSnippet(newWeb, name, desc, attrs, values) # Builds the snippet.
            
            # Updates the file.
            for ele in snippet: file.write(f"{ele}")

file.write("}") # For the last file.