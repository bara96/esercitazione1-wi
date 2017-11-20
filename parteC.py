from numpy import zeros
from plotly.utils import numpy
from scipy.linalg import svd
from math import log
from numpy import asarray, sum

class ParteC:
    # inizializza variabili
    def __init__(self, ignorechars="''',:'!''", stopwords=['and','edition','for','in','little','of','the','to']):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0

    def readStopwords(self):
        self.stopwords = list()
        with open("stopwords-en.txt", "r") as f:
            print("Leggendo file 'stopwords-en.txt'...")
            for line in f.readlines():
                for word in line.split():
                    self.stopwords.append(word)         # salva le stopWords lette
            f.close()

    def parse(self, doc):
        words = doc.split()
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if not w in self.stopwords:
                if w in self.wdict:
                    self.wdict[w].append(self.dcount)
                else:
                    self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):
        keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        keys.sort()
        self.A = zeros([len(keys), self.dcount])
        for i, k in enumerate(keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1

    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i, j] = (self.A[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def calc(self):
        self.U,self.S,self.Vt = svd(self.A)

    def exe(self):
        titles =["The Neatest Little Guide to Stock Market Investing",
                 "Investing For Dummies, 4th Edition",
                 "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
                 "The Little Book of Value Investing",
                 "Value Investing: From Graham to Buffett and Beyond",
                 "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
                 "Investing in Real Estate, 5th Edition",
                 "Stock Investing For Dummies",
                 "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"]
        self.readStopwords()
        for t in titles:
            self.parse(t)
        self.build()
        self.TFIDF()
        print self.A
