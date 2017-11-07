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

news_dir = 'news'
connection = urllib.urlopen('http://ricerca.repubblica.it/repubblica/topic/luoghi/i/italia')
dom = lxml.html.fromstring(connection.read())

if not os.path.dirname(news_dir):
    os.makedirs(news_dir)

with open("URLS.txt", "w") as f:
    num_urls = 0
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        f.write(link+"\n")
        num_urls = num_urls+1
    f.close()

with open('URLS.txt', "r") as f:
    urls = [f.readline().strip() for _ in range(num_urls)]

path = {}

for url in urls: #crea i file
  filename = re.sub('[^a-zA-Z0-9]', '-', url)
  filepath = os.path.join(news_dir, filename)
  path[url] = filepath

if not os.path.exists(filepath):
    print ('Scaricando {}'.format(url))
    urllib.urlretrieve(url, filepath)
    time.sleep(1)

news = {}

for (url, filepath) in path.items():
    with io.open(filepath, encoding='utf-8') as f:
        try:
            title, content = extract_page(f.read())
        except Exception as e:
            print 'Unexpected page structure!\n{}\n{}\n{}\n'.format(e.message, url, filepath)
            continue
    text = u'{}\n{}'.format(title," "+ content)
    news[url] = text

#print (news[urls[num_urls-1]])