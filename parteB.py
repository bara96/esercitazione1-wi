import re
from collections import defaultdict
from gensim.utils import lemmatize


class ParteB:
    # inizializza connessione e variabili
    def __init__(self):
        self.dictionary = defaultdict(int)
        self.frequentsWords = {}
        self.stopWords = list()

    # parte B1, legge il file e costruisce un dizionario delle parole trovate
    def readFile(self):
        with open("dati_salvati.txt", "r") as f:
            print("Leggendo il file 'dati_salvati.txt'...")
            for line in f.readlines():
                for word in line.split():
                        if not re.sub('[^a-zA-Z0-9]', '', word) is '':
                            self.dictionary[word] += 1
        f.close()

    # trova le 500 parole piu frequenti e le scrive su filec con la loro frequenza
    def findWords(self):
        self.frequentsWords = sorted(self.dictionary.iteritems(), key=lambda x: int(x[1]))
        self.frequentsWords.reverse()
        while len(self.frequentsWords) > 500:
            self.frequentsWords.pop()
        with open("parole_frequenti.txt", "w") as f:
            print("Scrivendo file 'parole_frequenti.txt'...")
            for word in self.frequentsWords:
                f.write(word[0] + " " + str(word[1]) + "\n")
        f.close()

    # legge il file stopwords-en e crea un file parole_modificate con le parole eliminate e sostituite
    def deleteStopWords(self):
        with open("stopwords-en.txt", "r") as f:
            print("Leggendo file 'stopwords-en.txt'...")
            for line in f.readlines():
                for word in line.split():
                    self.stopWords.append(word)         # salva le stopWords lette
        f.close()
        with open("paole_modificate.txt", "w") as f:
            print("Scrivendo file 'parole_modificate.txt'...")
            for word in self.frequentsWords:
                if not(word[0] in self.stopWords):
                    if not(u''.join(lemmatize(word[0])).encode('utf-8').strip() is ""):
                        f.write(u''.join(lemmatize(word[0])).encode('utf-8').strip() + "\n")   # sostituisce le parole non in stopWords, quelle presenti le ignora
        f.close()

    def main(self):
        self.readFile()
        self.findWords()
        self.deleteStopWords()

