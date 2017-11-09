import re
from collections import defaultdict
from gensim.utils import lemmatize


class ParteB:
    # inizializza connessione e variabili
    def __init__(self):
        self.dictionary = defaultdict(int)
        self.wordsList = {}
        self.stopWords = list()

    #parte B1, legge il file e costruisce un dizionario delle parole trovate
    def readFile(self):
        with open("dati_salvati.txt", "r") as f:
            for line in f.readlines():
                for word in line.split():
                    self.dictionary[str(word)] += 1
        f.close()

    # trova le 500 parole piu frequenti e le scrive su filec con la loro frequenza
    def findWords(self):
        self.wordsList = sorted(self.dictionary.iteritems(), key=lambda x: int(x[1]))
        self.wordsList.reverse()
        while len(self.wordsList)>500:
            self.wordsList.pop()
        with open("parole_frequenti.txt", "w") as f:
            for word in self.wordsList:
                f.write(re.sub('[^a-zA-Z0-9 ]', '', str(word))+"\n")
        f.close()

    # legge il file stopwords-en e crea un file dati_modificati con le parole eliminate e sostituite
    def deleteStopWords(self):
        with open("stopwords-en.txt", "r") as f:
            for line in f.readlines():
                for word in line.split():
                    self.stopWords.append(word)         # salva le stopWords lette
        f.close()
        with open("dati_salvati.txt", "r") as f:
            text = ""
            for line in f.readlines():
                for word in line.splitlines(True):
                    if not(word in self.stopWords):
                        text += " ".join(lemmatize(word))   # sostituisce le parole non in stopWords, quelle presenti le ignora
                text += "\n"
        f.close()
        with open("dati_modificati.txt", "w") as f:
                f.write(text)
        f.close()

    def main(self):
        self.readFile()
        self.findWords()
        self.deleteStopWords()
