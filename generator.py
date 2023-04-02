import requests
import re
import os

from bs4 import BeautifulSoup

def requestWeb():
    request = requests.get("https://origins.readthedocs.io/en/latest/types/power_types/", headers={"User-Agent": "Mozilla/5.0"})  # Requests access
    return BeautifulSoup(request.text, 'html.parser')

def filterWeb(htmlSpoon):
    spoonedDiv = htmlSpoon.find_all(["ul", "h3"], attrs={'class': None})
    spoonedDiv = htmlSpoon.find_all(["a", "h3"], attrs={'class': None})
    return spoonedDiv

res = filterWeb(requestWeb())
for tag in res:
    reg = re.compile('<a.*href="(?!\\.)(?!http)([a-zA-Z].*)">(.*)</a>|<h3.*>(.*)</h3>').search(str(tag))
    if reg:
        print(reg.groups())

# for tag in res:
#     print(tag)