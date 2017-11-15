import io
import os
import re
from collections import defaultdict
import operator
from math import sqrt
from plotly.utils import numpy
from parteA import ParteA
from parteB import ParteB

class ParteC:
    # inizializza variabili
    def __init__(self, urls):
        self.urls = urls    # i miei 20 url
        self.numDocs = 0    # numero di documenti su cui si esegue la ricerca
        self.keyWords = dict()  # key words dei 20 url
        self.wordsFreqList = list()  # lista dei dizionari con le frequenze delle parole
        self.urlList = list()   #url corrispondenti a wordsFreqList
        self.wordsOccurrences = defaultdict(int) # dizionario per contare in quanti documenti appare ogni parola

    # ricerca nei documenti scaricati le parole chiave, e  restituisce una lista di dizionari (uno per documento) con le orccorrenze delle parole cercate
    # inoltre aggiorna il docCount tenendo conto in quanti  documenti appaiono le parole
    def countWords(self, words):    # words = dict["word"]:freq
        # searchText = ""
        # for word in words:
        #     searchText += word+"+"
        # cerca = ParteA("http://www.reuters.com/search/news?blob="+searchText, "search/", "search_dati.txt", True, 10)
        # cerca.exe()
        parteA = ParteA()
        self.numDocs = parteA.urlsCount()
        urls = parteA.urlsReader(self.numDocs)
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
                                self.wordsOccurrences[word] += 1    # aumento il contatore (conto in quanti documenti appare)
                        self.urlList.append(url)    # salvo l'url corrispondente
                        self.wordsFreqList.append(dictionary)   # salvo il dizionario nella lista e passo al prossimo documento
                        f.close()
            except Exception as e:
                print str(e)

    def tf_calculation(self, words_frequency):  # words_frequency = dict["word"]:freq ,calcola il tf delle parole e restituisce dict[word]=val
        tf = dict()
        for (word, freq) in words_frequency.iteritems():
            if freq == 0:
                tf[word] = 0
            else:
                tf[word] = round(1 + numpy.log10(freq), 5)
        return tf

    def idf_calculation(self, df):   # df = dict["word"]:occurrences , restituisce un dizionario dell'idf delle df dict[word]=val
        idf = dict()
        for (word, occurrences) in df.iteritems():
            if occurrences == 0:
                idf[word] = 0
            else:
                idf[word] = round(numpy.log10(self.numDocs/occurrences), 5)
        return idf

    def vectorLength_calculation(self, tf): # tf = dict["word"]:freq calcola il vettore corrispondente
        vector = 0
        for (word, freq) in tf.iteritems():
            vector += pow(freq, 2)
        return round(sqrt(vector), 5)

    def normalize(self, tf, vector_length): # tf = dict["word"]:freq, int, restituisce il dizionario tf normalizzato
        norm = dict()
        for (word, freq) in tf.iteritems():
            norm[word] = round(freq/vector_length, 5)
        return norm

    def cos_distance(self, dict1, dict2):   #dict = dict["word"]:freq ,restituisce la distanza a similarita coseno
        cos = 0
        for (word, value) in dict1.iteritems():
            cos += round(dict1[word] * dict2[word], 5)
        return cos


    def calculate(self, words_freq_list): # words_freq_list = list(dict["word"]:freq) ,restituisce la lista di dizionari con il tf normalizzato
        calc_tf = list()
        for dict in words_freq_list:
            calc_tf.append(self.tf_calculation(dict))
        calc_norm = list()
        for dict in calc_tf:
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
            self.keyWords[word[0]] = word[1]

        self.countWords(self.keyWords)
        key_idf = self.idf_calculation(self.wordsOccurrences)
        key_tf = self.tf_calculation(self.keyWords)
        key_norm = self.normalize(key_tf, self.vectorLength_calculation(key_tf))
        wordsNormList = self.calculate(self.wordsFreqList)
        print self.cos_distance(key_norm, wordsNormList[0])
        print wordsNormList
        print self.urlList
