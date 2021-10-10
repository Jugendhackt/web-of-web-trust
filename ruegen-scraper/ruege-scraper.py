# ruegen
# By Melly

from bs4 import BeautifulSoup
import html_text
from requests import get, post
import re
from os import getenv

SPACER = "=" * 20


class RuegenCollector:
    url: str

    def __init__(self):
        host = getenv("API_HOST") or "0.0.0.0"
        port = getenv("API_PORT") or 8080
        path = getenv("API_RUEGEN_PATH") or "/ruegen/update/"
        ssl = getenv("API_SSL") or False

        if ssl:
            self.url = f"https://{host}:{port}/{path}"
        else:
            self.url = f"http://{host}:{port}/{path}"

    def push(self, medium: str, aktenzeichen: str, title: str, ziffer: str, year: int):
        """Push Ruege to API. This is done with the pre-evaluated URL"""
        try:
            post(
                self.url,
                json=dict(
                    medium=medium,
                    aktenzeichen=aktenzeichen,
                    title=title,
                    ziffer=ziffer,
                    year=year,
                ),
            )
        except Exception as e:
            print(
                f"{SPACER}\nError when pushing ruege to server\n{SPACER}\n{e}\nAttempting to continue\n"
            )

    def getruegen(self):
        url = "https://www.presserat.de/ruegen-presse-uebersicht.html"
        page = get(url)

        main = BeautifulSoup(page.text, "html.parser").find("main")

        for section in main.find_all("section"):
            # divs are seperated with year being on the left and the content on the right
            year_div, content_div = section.find_all("div", recursive=False)
            year = int(year_div.text.strip())

            # extract text from content div
            txt = html_text.extract_text(str(content_div))

            for line in txt.splitlines():
                if "(" in line:
                    medium, line = line.split("(", 1)
                    aktenzeichen, line = re.split("[,\)]", line, 1)
                    if '"' in line or "'" in line:
                        line = line.lstrip(": ")
                        title, line = line.split(",", 1)
                    else:
                        title = ""
                    line = line.lstrip(", ")
                    iffer = line.split(",")[0]
                    self.push(medium.strip(), aktenzeichen, title, iffer, year)

if __name__ == "__main__":
    r = RuegenCollector()
    r.getruegen()
