# ruegen

import requests
from bs4 import BeautifulSoup
import html_text
import re

url: str = "https://www.presserat.de/ruegen-presse-uebersicht.html"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
main = soup.find('main')

for section in main.find_all('section'):
    div1, div2 = section.find_all('div', recursive=False)
    year = div1.text.strip()
    txt = html_text.extract_text(str(div2))
    for line in txt.splitlines():
        if "(" in line:
            medium, line = line.split('(', 1)
            az, line = re.split("[,\)]", line, 1)
            if '"' in line or "'" in line:
                line = line.lstrip(": ")
                title,line = line.split (",",1)
            else:
                title = ""
            line = line.lstrip (", ")
            iffer = line.split(",") [0]
            #temp, line = re.split('[\'"]', line, 1)
                #titel, line = re.split('[\'"]', line, 1)
            print(medium,az,title,iffer)
