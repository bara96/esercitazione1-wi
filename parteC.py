from parteA import ParteA
from parteB import ParteB


class ParteC:
    # inizializza variabili
    def __init__(self, urls):
        self.urls = urls

    def exe(self):
        parteA = ParteA("", "news20/", "dati_salvati2.txt", False, 20)
        parteA.setUrls(self.urls)
        parteA.exe()
        parteB = ParteB("dati_salvati2.txt", "parole_frequenti2.txt", "parole_modificate2.txt", False)
        parteB.exe()
