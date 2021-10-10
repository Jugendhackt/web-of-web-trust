# ruegen library
import requests

class Ruege:
    name: str

    def __init__(self, name: str):
        self.name = name

    def ruege(self):

        files = {
            'start': 0,
            'limit': 200,
            'volltext': self.name,
            'aktenzeichen': "",
            'ziffer': "",
            'entscheidung': "",
            's_jahr': "",
            'e_jahr': "",
            'sort': "a.jahr",
            'dir': "ASC",
            }

        response = requests.post('https://recherche.presserat.info/index.php/main/search', data=files)

        x = response.json()
        x = x['results']
        return x


#print(Ruege("spiegel").ruege())
