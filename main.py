import os
import re
import time
import urllib
import bs4
import io
import lxml.html

def extract_page(page_hmtl):
    page_soup = bs4.BeautifulSoup(page_hmtl, 'html.parser')
    head = page_soup.find('div', class_= 'header-content')
    title = page_soup.find('h1').get_text(strip=True)
    content = page_soup.find('div').get_text(strip=True)
    return title, content

#inizializza connessione e variabili
news_dir = 'news/'
path = {}
news = {}
connection = urllib.urlopen('http://ricerca.repubblica.it/')
dom = lxml.html.fromstring(connection.read())

#controlla/crea directory news
if not os.path.isdir(news_dir):
    os.makedirs(news_dir)

#apre URLS.txt in scrittura, legge dal dom (sito) la pagina e scrive su URLS tutti gli href chhe trova
with open("URLS.txt", "w") as f:
    num_urls = 0
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        f.write(link+"\n")
        num_urls = num_urls+1
    f.close()

#apre URLS e legge i link
with open('URLS.txt', "r") as f:
    urls = [f.readline().strip() for _ in range(num_urls)]
    f.close()

for url in urls: #crea i file dagli url
    filename = re.sub('[^a-zA-Z0-9]', '', url)
    filepath = os.path.join(news_dir, filename)
    path[url] = filepath
    if not os.path.exists(filepath):
        try:
            print ('Scaricando {}'.format(url))
            urllib.urlretrieve(url, filepath)
            time.sleep(1)
        except Exception as e:
            print str(e)
            continue

#legge i file da
for (url, filepath) in path.items():
    try:
        with io.open(filepath, encoding='utf-8') as f:
            title, content = extract_page(f.read())
            text = u'{}\n{}'.format(title, content)
            news[url] = text
    except Exception as e:
        print str(e)
        continue

for file in news:
    print (file)