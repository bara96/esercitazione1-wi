import re
from collections import defaultdict
from gensim.utils import lemmatize as lem
import matplotlib.pyplot as plt
import plotly as py

class ParteB:
    # inizializza variabili
    def __init__(self, filename_data="dati_salvati.txt", filename_frequent="parole_frequenti.txt", filename_frequent_modified="parole_modificate.txt", show_graph=True, lemmatize=True):    # grafico = sceglie se visualizzare o no il grafico
        # nomi dei file in cui leggere / salvare dati e frequenze
        self.filename_data = filename_data
        self.filename_frequent1 = filename_frequent
        self.filename_frequent2 = filename_frequent_modified
        # dizionari e liste
        self.dictionary = defaultdict(int)
        self.frequents_words = {}
        self.modified_words = list()
        self.stop_words = list()
        # boolean per visualizzare o no il grafico e per lemmatizzar o no le parole frequenti
        self.show_graph = show_graph
        self.lemmatize = lemmatize

    # parte B1, legge il file e costruisce un dizionario delle parole trovate
    def readFile(self):
        with open(self.filename_data, "r") as f:
            print("Leggendo il file {}...".format(self.filename_data))
            for line in f.readlines():
                for word in line.split():
                        if not re.sub('[^a-zA-Z0-9]', '', word) is "":
                            self.dictionary[re.sub('[^a-zA-Z0-9]', '', word.lower())] += 1
            f.close()

    # trova le 500 parole piu frequenti e le scrive su file con la loro frequenza
    def findWords(self):
        self.frequents_words = sorted(self.dictionary.iteritems(), key=lambda x: int(x[1]))
        self.frequents_words.reverse()
        while len(self.frequents_words) > 500:
            self.frequents_words.pop()
        with open(self.filename_frequent1, "w") as f:
            print("Scrivendo file {}...".format(self.filename_frequent1))
            for word in self.frequents_words:
                f.write(word[0] + " " + str(word[1]) + "\n")
            f.close()

    # legge il file stopwords-en e crea un file parole_modificate con le parole eliminate e sostituite
    def deleteStopWords(self, lemmatize):
        with open("stopwords-en.txt", "r") as f:
            print("Leggendo file 'stopwords-en.txt'...")
            for line in f.readlines():
                for word in line.split():
                    self.stop_words.append(word)         # salva le stopWords lette
            f.close()
        with open(self.filename_frequent2, "w") as f:
            print("Scrivendo file {}...".format(self.filename_frequent2))
            for word in self.frequents_words:
                if not(word[0] in self.stop_words):
                    if not(u''.join(lem(word[0])).encode('utf-8').strip() is ""):
                        if lemmatize:
                            self.modified_words.append((u''.join(lem(word[0])).encode('utf-8').strip(), word[1]))
                            f.write(u''.join(lem(word[0])).encode('utf-8').strip() + " " + str(word[1]) + "\n")   # sostituisce le parole non in stopWords, quelle presenti le ignora
                        else:
                            self.modified_words.append((u''.join(word[0]).encode('utf-8').strip(), word[1]))
                            f.write(u''.join(word[0]).encode('utf-8').strip() + " " + str(word[1]) + "\n")  # sostituisce le parole non in stopWords, quelle presenti le ignora
            f.close()

    def plotGraph(self, values, title):
        y = list()
        x = list()
        i = 1
        for value in values:
            y.append(int(value[1]))
            x.append(i)
            i += 1
        plt.bar(x, y, align='center')  # A bar chart
        plt.title(title)
        plt.xlabel("Rank")
        plt.ylabel("Frequenza")
        plt.show()
        fig = plt.gcf()
        #plot_url = py.plotly.plot_mpl(fig, filename='istogramma_parole1')

    def exe(self):
        py.tools.set_credentials_file(username='bara96', api_key='yxyk0sCwGD63aOsFaq3A')
        self.readFile()
        self.findWords()
        self.deleteStopWords(self.lemmatize)
        if self.show_graph:
            self.plotGraph(self.frequents_words, "Istogramma frequenza")
            self.plotGraph(self.modified_words, "Istogramma frequenza modificato")


    def getDictionary(self):
        return self.dictionary

    def setDictionary(self, dictionary):
        self.dictionary = dictionary

    def getFrequentsWords(self):
        return self.frequents_words

    def getModifiedWords(self):
        return self.modified_words

    def getStopWords(self):
        return self.stop_words

    def setStopWords(self, stopWords):
        self.stop_words = stopWords
