import io
import os
import re
import time
import urllib
import bs4
import lxml.html
from bs4 import BeautifulSoup


class ParteA:
    # inizializza connessione e variabili
    def __init__(self, origin_url="http://www.reuters.com/resources/archive/us/20171101.html", download_directory="news/", filename_data="dati_salvati.txt", auto_download=True, download_limit=1000):
        # nome della cartella in cui salvare i dati
        self.download_directory = download_directory
        # nome del file in cui salvare dati
        self.filename_data = filename_data
        # conterra percorso delle pagine scariate
        self.path = {}
        # numero di url saricati
        self.num_urls = 0
        # url 'origine' da cui scaricare
        self.origin_url = origin_url
        # memorizza tutti gli urls scaricati e scritti sul file URLS
        self.urls = list()
        # true = scarica tutte le sottopagine da  origin_url, false = imposta una lista di pagine da scaricare su urls
        self.auto_download = auto_download
        # limita il download a n pagine
        self.download_limit = download_limit

    def extractPage(self, page_hmtl):
        # page_soup = bs4.BeautifulSoup(page_hmtl, 'html.parser')
        soup = BeautifulSoup(page_hmtl, 'html.parser')
        # head = page_soup.find('div', class_='header-content')
        title = u''.join(soup.title.string).encode('utf-8').strip()
        content = ""
        div = soup.find('div', attrs={"class": "ArticleBody_body_2ECha"})
        for p in div.findAll('p'):
                content += u''.join(p.text).encode('utf-8').strip()
        return title, content

    # costruisce il file URLS
    def urlsMaker(self):
        # controlla/crea directory
        connection = urllib.urlopen(self.origin_url)
        dom = lxml.html.fromstring(connection.read())
        # apre URLS.txt in scrittura, legge dal dom (sito) la pagina e scrive su URLS tutti gli href che trova
        with open("URLS.txt", "w") as f:
            print("Scrivendo file 'URLS.txt'...")
            self.num_urls = 0
            for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
                if not link.find("article") == -1:
                    if not link.find("http") == -1:
                        f.write(link + "\n")
                    else:
                        f.write("http://www.reuters.com"+link + "\n")
                self.num_urls = self.num_urls + 1
            f.close()

    #  legge il file URLS e restituisce gli url letti
    def urlsReader(self, numUrls):
        with open('URLS.txt', "r") as f:
            print("Leggendo file 'URLS.txt'...")
            urls = [f.readline().strip() for _ in range(numUrls)]
            f.close()
        return urls
    # conta il numero di url salvati in URLS.txt
    def urlsCount(self):
        n = 0
        with open('URLS.txt', "r") as f:
            print("Leggendo file 'URLS.txt'...")
            while f.readline():
                n += 1
            f.close()
        return n

    # scarica le pagine dagli URLS e le salva nella cartella news
    def pageDownolader(self, urls):
        if not os.path.isdir(self.download_directory):
            os.makedirs(self.download_directory)
        for url in urls:
            if self.download_limit <= 0:
                break
            filename = re.sub('[^a-zA-Z0-9]', '', url)
            filepath = os.path.join(self.download_directory, filename)
            self.path[url] = filepath
            if not os.path.exists(filepath):
                try:
                    print ('Scaricando {}...'.format(url))
                    urllib.urlretrieve(url, filepath)
                    self.download_limit -= 1
                    time.sleep(0.2)
                except Exception as e:
                    print str(e)

    # legge i file dalla cartella 'news' e scrive su file titolo e contenuto
    def dataWriter(self):
        i = 1
        with open(self.filename_data, "w") as dati:
            print("Scrivendo file {}...".format(self.filename_data))
            for (url, filepath) in self.path.items():
                try:
                    if os.path.exists(filepath):
                        with io.open(filepath, encoding='utf-8') as f:
                            #print("Leggendo file da {}...".format(filepath))
                            title, content = self.extractPage(f.read())
                            dati.write(str(i)+") "+str(title)+"\n")
                            dati.write(str(content)+"\n")
                            i = i + 1
                            f.close()
                except Exception as e:
                    print str(e)
            dati.close()

    # parte A1-A2
    def exe(self):
        if self.auto_download:
            self.urlsMaker()
            self.urls = self.urlsReader(self.num_urls)
        self.pageDownolader(self.urls)
        self.dataWriter()

    def getUrls(self):
        return self.urls

    def setUrls(self, urls):
        self.urls = urls

    def setOriginUrl(self):
        return self.origin_url

    def setOriginUrls(self, origin_url):
        self.origin_url = origin_url

    def getNumUrls(self):
        return self.num_urls

    def setNumUrls(self, numUrls):
        self.num_urls = numUrls


