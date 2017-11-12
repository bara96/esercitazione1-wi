from parteA import ParteA
from parteB import ParteB
from parteC import ParteC

c = 0
while not(c == 1 or c == 2 or c == 3):
    c = input("1)ParteA 2)ParteB 3)ParteC \n")

if c == 1:
    # archivio notizie: http://www.reuters.com/resources/archive/us/
    parteA = ParteA('http://www.reuters.com/resources/archive/us/20171101.html', "news/", "dati_salvati.txt", True, 1000)
    parteA.exe()
if c == 2:
    parteB = ParteB("dati_salvati.txt", "parole_frequenti.txt", "parole_modificate.txt", True)
    parteB.exe()

    # https://www.analyticsvidhya.com/blog/2015/08/beginners-guide-learn-content-based-recommender-systems/
if c == 3:
    urls20 = list()
    urls20.append("http://www.reuters.com/article/us-asean-summit/gala-glitz-masks-asias-tensions-as-trump-winds-up-tour-idUSKBN1DC07P")
    urls20.append("http://www.reuters.com/article/us-mideast-crisis-syria-israel/israel-signals-free-hand-in-syria-as-u-s-russia-expand-truce-idUSKBN1DC0HY?il=0")
    urls20.append("http://www.reuters.com/article/us-france-security/france-frets-over-internal-threat-two-years-after-paris-attacks-idUSKBN1DC0Q2")
    urls20.append("http://www.reuters.com/article/us-trump-asia-usa-russia/trump-distances-himself-from-remarks-on-putin-over-election-meddling-idUSKBN1DC031")
    urls20.append("http://www.reuters.com/article/us-trump-asia-northkorea/trump-says-north-koreas-kim-insulted-him-by-calling-him-old-idUSKBN1DC00Y")
    parteC = ParteC(urls20)
    parteC.exe()