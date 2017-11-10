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
    def __init__(self, url):
        self.news_dir = 'news/'
        # self.news_title = list()
        # self.news_content = list()
        self.path = {}
        self.num_urls = 0
        self.url = url

    def extract_page(self, page_hmtl):
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
    def URLS_maker(self):
        # controlla/crea directory
        if not os.path.isdir(self.news_dir):
            os.makedirs(self.news_dir)
        connection = urllib.urlopen(self.url)
        dom = lxml.html.fromstring(connection.read())
        # apre URLS.txt in scrittura, legge dal dom (sito) la pagina e scrive su URLS tutti gli href che trova
        with open("URLS.txt", "w") as f:
            print("Scrivendo file 'URLS.txt'...")
            self.num_urls = 0
            for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
                if not link.find("article") == -1:
                   f.write(link + "\n")
                self.num_urls = self.num_urls + 1
            f.close()

    #  legge il file URLS e restituisce gli url letti
    def URLS_reader(self):
        with open('URLS.txt', "r") as f:
            print("Leggendo file 'URLS.txt'...")
            urls = [f.readline().strip() for _ in range(self.num_urls)]
            f.close()
        return urls

    # scarica le pagine dagli URLS e le salva nella cartella news
    def page_downolader(self):
        urls = self.URLS_reader()
        limit = 1000
        for url in urls:
            if limit == 0:
                break
            filename = re.sub('[^a-zA-Z0-9]', '', url)
            filepath = os.path.join(self.news_dir, filename)
            self.path[url] = filepath
            if not os.path.exists(filepath):
                try:
                    print ('Scaricando {}...'.format(url))
                    urllib.urlretrieve(url, filepath)
                    limit -= 1
                    time.sleep(0.1)
                except Exception as e:
                    print str(e)

    # legge i file dalla cartella e scrive su file titolo e contenuto
    def data_writer(self):
        i = 0
        with open("dati_salvati.txt", "w") as dati:
            print("Scrivendo file 'dati_salvati.txt'...")
            for (url, filepath) in self.path.items():
                try:
                    if os.path.exists(filepath):
                        with io.open(filepath, encoding='utf-8') as f:
                            #print("Leggendo file da {}...".format(filepath))
                            title, content = self.extract_page(f.read())
                            dati.write(str(i)+") "+str(title)+"\n")
                            # print "titolo: " + str(title)
                            dati.write(str(content)+"\n")
                            # print "contenuto: " + str(content)
                            i = i + 1
                            f.close()
                except Exception as e:
                    print str(e)
            dati.close()

    # parte A1-A2
    def main(self):
        self.URLS_maker()
        self.page_downolader()
        self.data_writer()