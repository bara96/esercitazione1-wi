import io
import os
import re
from collections import defaultdict
import operator
from math import sqrt
from plotly.utils import numpy
from parteA import ParteA
from parteB import ParteB

class ParteB3:
    # inizializza variabili
    def __init__(self, urls):
        self.urls = urls    # i miei 20 url
        self.num_docs = 0    # numero di documenti su cui si esegue la ricerca
        self.key_words = dict()  # key words dei 20 url
        self.words_freq_list = list()  # lista dei dizionari con le frequenze delle parole
        self.url_list = list()   #url corrispondenti a wordsFreqList
        self.words_occurrences = defaultdict(int) # dizionario per contare in quanti documenti appare ogni parola

    # ricerca nei documenti scaricati le parole chiave, e  restituisce una lista di dizionari (uno per documento) con le orccorrenze delle parole cercate
    # inoltre aggiorna il words_occurrences tenendo conto in quanti  documenti appare ogni parola.
    def countWords(self, words):    # words = dict["word"]:freq
        # searchText = ""
        # for word in words:
        #     searchText += word+"+"
        # cerca = ParteA("http://www.reuters.com/search/news?blob="+searchText, "search/", "search_dati.txt", True, 10)
        # cerca.exe()
        parteA = ParteA()
        self.num_docs = parteA.urlsCount()
        urls = parteA.urlsReader(self.num_docs)
        path = {}
        for url in urls:    #costruisce le path dagli url
            filename = re.sub('[^a-zA-Z0-9]', '', url)
            filepath = os.path.join("news/", filename)
            path[url] = filepath

        # sorted_path = sorted(path.items(), key=operator.itemgetter(1)) # ordino url
        for (url, filepath) in path.iteritems():    #  crea i dizionari da aggiungere a wordsFreqList
            dictionary = dict()
            try:
                if os.path.exists(filepath):
                    with io.open(filepath, encoding='utf-8') as f:
                        title, content = parteA.extractPage(f.read())
                        tit = title.lower()     # converte title, content in minuscolo per il confronto
                        con = content.lower()
                        for (word, freq) in words.iteritems():  # per ogni parola chiave
                            n = int(tit.count(word)) + int(con.count(word)) # conto le sue occorrenze nel documento
                            dictionary[word] = n    #la salvo nel dizionario con le sue occorrenze
                            if n > 0:   # se ne ho trovata almeno una
                                self.words_occurrences[word] += 1    # aumento il contatore (conto in quanti documenti appare)
                        self.url_list.append(url)    # salvo l'url corrispondente
                        self.words_freq_list.append(dictionary)   # salvo il dizionario nella lista e passo al prossimo documento
                        f.close()
            except Exception as e:
                print str(e)

    # words_frequency = dict["word"]:freq ,calcola il tf delle parole e restituisce dict[word]=val
    def tf_calculation(self, words_frequency, idf):
        tf = dict()
        for (word, freq) in words_frequency.iteritems():
            if freq == 0:
                tf[word] = 0
            else:
                tf[word] = round(freq * idf[word], 5)
        return tf

    # df = dict["word"]:occurrences , restituisce un dizionario dell'idf delle df dict[word]=val
    def idf_calculation(self, df):
        idf = dict()
        for (word, occurrences) in df.iteritems():
            if occurrences == 0:
                idf[word] = 0
            else:
                idf[word] = round(numpy.log10(self.num_docs / occurrences), 5)
        return idf

    # tf = dict["word"]:freq calcola il vettore corrispondente
    def vectorLength_calculation(self, tf):
        vector = 0
        for (word, freq) in tf.iteritems():
            vector += pow(freq, 2)
        return round(sqrt(vector), 5)

    # tf = dict["word"]:freq, int, restituisce il dizionario tf normalizzato
    def normalize(self, tf, vector_length):
        norm = dict()
        for (word, freq) in tf.iteritems():
                norm[word] = round(freq/vector_length, 5)
        return norm

    # dict = dict["word"]:freq ,restituisce la distanza a similarita coseno
    def cos_distance(self, dict1, dict2):
        cos = 0
        for (word, value) in dict1.iteritems():
            cos += round(dict1[word] * dict2[word], 5)
        return cos

    # words_freq_list = list(dict["word"]:freq) ,restituisce la lista di dizionari con il tf normalizzato
    def calculate(self, words_freq_list, idf):
        calc_tf = list()
        for dict in words_freq_list:
            calc_tf.append(self.tf_calculation(dict, idf))
        calc_norm = list()
        for dict in calc_tf:
            if self.vectorLength_calculation(dict) > 0:  # scarto i documenti con vettore di lunghezza 0, perche' significa che non vi sono elementi chiate nel documento
                calc_norm.append(self.normalize(dict, self.vectorLength_calculation(dict)))
        return calc_norm

    def exe(self):
        parteA = ParteA(download_directory="news20/", filename_data="dati_salvati2.txt", auto_download=False, download_limit=20)
        parteA.setUrls(self.urls)
        parteA.exe()
        parteB = ParteB(filename_data="dati_salvati2.txt", filename_frequent="parole_frequenti2.txt", filename_frequent_modified="parole_modificate2.txt", show_graph=False, lemmatize=False)
        parteB.exe()
        words = parteB.getModifiedWords()
        while len(words) > 5:   #tengo solo le 5 piu frequenti
            words.pop()

        for word in words:
            self.key_words[word[0]] = word[1]

        self.countWords(self.key_words)
        key_idf = self.idf_calculation(self.words_occurrences)
        key_tf = self.tf_calculation(self.key_words, key_idf)
        key_norm = self.normalize(key_tf, self.vectorLength_calculation(key_tf))
        wordsNormList = self.calculate(self.words_freq_list, key_idf)
        distance = dict()
        for i in range(0, len(wordsNormList)-1):
            distance[self.url_list[i]] = self.cos_distance(key_norm, wordsNormList[i])
        suggest = sorted(distance.items(), key=operator.itemgetter(1)) # ordino per coseni

        print "suggerimenti migliori trovati: "
        for i in range(len(suggest)-11, len(suggest)-1):
            print suggest[i]
