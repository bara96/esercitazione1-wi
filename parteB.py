import re
from collections import defaultdict
from gensim.utils import lemmatize as lem
import matplotlib.pyplot as plt
import plotly as py

class ParteB:
    # inizializza variabili
    def __init__(self, filename_data="dati_salvati.txt", filename_frequent="parole_frequenti.txt", filename_frequent_modified="parole_modificate.txt", show_graph=True, lemmatize=True):    # grafico = sceglie se visualizzare o no il grafico
        # nomi dei file in cui salvare dati e frequenze
        self.filenameData = filename_data
        self.filenameFrequent1 = filename_frequent
        self.filenameFrequent2 = filename_frequent_modified
        # dizionari e liste
        self.dictionary = defaultdict(int)
        self.frequentsWords = {}
        self.modifiedWords = list()
        self.stopWords = list()
        # boolean per visualizzare o no il grafico e per lemmatizzar o no le parole frequenti
        self.showGraph = show_graph
        self.lemmatize = lemmatize

    # parte B1, legge il file e costruisce un dizionario delle parole trovate
    def readFile(self):
        with open(self.filenameData, "r") as f:
            print("Leggendo il file {}...".format(self.filenameData))
            for line in f.readlines():
                for word in line.split():
                        if not re.sub('[^a-zA-Z0-9]', '', word) is "":
                            self.dictionary[re.sub('[^a-zA-Z0-9]', '', word.lower())] += 1
            f.close()

    # trova le 500 parole piu frequenti e le scrive su file con la loro frequenza
    def findWords(self):
        self.frequentsWords = sorted(self.dictionary.iteritems(), key=lambda x: int(x[1]))
        self.frequentsWords.reverse()
        while len(self.frequentsWords) > 500:
            self.frequentsWords.pop()
        with open(self.filenameFrequent1, "w") as f:
            print("Scrivendo file {}...".format(self.filenameFrequent1))
            for word in self.frequentsWords:
                f.write(word[0] + " " + str(word[1]) + "\n")
            f.close()

    # legge il file stopwords-en e crea un file parole_modificate con le parole eliminate e sostituite
    def deleteStopWords(self, lemmatize):
        with open("stopwords-en.txt", "r") as f:
            print("Leggendo file 'stopwords-en.txt'...")
            for line in f.readlines():
                for word in line.split():
                    self.stopWords.append(word)         # salva le stopWords lette
            f.close()
        with open(self.filenameFrequent2, "w") as f:
            print("Scrivendo file {}...".format(self.filenameFrequent2))
            for word in self.frequentsWords:
                if not(word[0] in self.stopWords):
                    if not(u''.join(lem(word[0])).encode('utf-8').strip() is ""):
                        if lemmatize:
                            self.modifiedWords.append((u''.join(lem(word[0])).encode('utf-8').strip(), word[1]))
                            f.write(u''.join(lem(word[0])).encode('utf-8').strip() + " " + str(word[1]) + "\n")   # sostituisce le parole non in stopWords, quelle presenti le ignora
                        else:
                            self.modifiedWords.append((u''.join(word[0]).encode('utf-8').strip(), word[1]))
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
        if self.showGraph:
            self.plotGraph(self.frequentsWords, "Istogramma frequenza")
            self.plotGraph(self.modifiedWords, "Istogramma frequenza modificato")


    def getDictionary(self):
        return self.dictionary

    def setDictionary(self, dictionary):
        self.dictionary = dictionary

    def getFrequentsWords(self):
        return self.frequentsWords

    def getModifiedWords(self):
        return self.modifiedWords

    def getStopWords(self):
        return self.stopWords

    def setStopWords(self, stopWords):
        self.stopWords = stopWords
