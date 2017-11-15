from parteA import ParteA
from parteB import ParteB
from parteC import ParteC

c = 0
while not(c == 1 or c == 2 or c == 3):
    c = input("1)ParteA 2)ParteB 3)ParteC \n")

if c == 1:
    # archivio notizie: http://www.reuters.com/resources/archive/us/
    parteA = ParteA()
    parteA.exe()
if c == 2:
    parteB = ParteB()
    parteB.exe()

    # https://www.analyticsvidhya.com/blog/2015/08/beginners-guide-learn-content-based-recommender-systems/
if c == 3:
    urls20 = list()
    urls20.append("http://www.reuters.com/article/us-asean-summit/gala-glitz-masks-asias-tensions-as-trump-winds-up-tour-idUSKBN1DC07P")
    urls20.append("http://www.reuters.com/article/us-mideast-crisis-syria-israel/israel-signals-free-hand-in-syria-as-u-s-russia-expand-truce-idUSKBN1DC0HY?il=0")
    urls20.append("http://www.reuters.com/article/us-france-security/france-frets-over-internal-threat-two-years-after-paris-attacks-idUSKBN1DC0Q2")
    urls20.append("http://www.reuters.com/article/us-trump-asia-usa-russia/trump-distances-himself-from-remarks-on-putin-over-election-meddling-idUSKBN1DC031")
    urls20.append("http://www.reuters.com/article/us-trump-asia-northkorea/trump-says-north-koreas-kim-insulted-him-by-calling-him-old-idUSKBN1DC00Y")
    urls20.append("http://www.reuters.com/article/us-trump-asia-philippines/trump-and-duterte-bond-at-asia-summit-u-s-says-rights-mentioned-briefly-idUSKBN1DD0FZ")
    urls20.append("http://www.reuters.com/article/us-trump-effect-agriculture-automation/as-trump-targets-immigrants-u-s-farm-sector-looks-to-automate-idUSKBN1DA0IQ")
    urls20.append("http://www.reuters.com/article/us-wall-street-compensation/wall-street-bonuses-may-jump-10-percent-this-year-report-idUSKBN1DD02C")
    urls20.append("http://www.reuters.com/article/us-time-warner-m-a-at-t/trumps-cnn-attacks-may-hobble-legal-case-to-block-att-time-warner-deal-idUSKBN1D92HF")
    urls20.append("http://www.reuters.com/article/us-global-forests/forest-fires-stoke-record-loss-in-world-tree-cover-monitor-idUSKBN1CS20Z")
    urls20.append("http://www.reuters.com/article/us-southkorea-trade-solar/south-korea-may-consider-filing-wto-complaint-over-u-s-solar-tariffs-idUSKBN1D2115")
    urls20.append("http://www.reuters.com/article/us-london-emissions/london-introduces-vehicle-pollution-levy-in-new-blow-to-diesel-idUSKBN1CR0YO")
    urls20.append("http://www.reuters.com/article/us-britain-iran-may/britain-considers-diplomatic-protection-for-jailed-aid-worker-in-iran-idUSKBN1DD1D1")
    urls20.append("http://www.reuters.com/article/us-singles-day-china-logistics/chinas-deliverymen-face-robot-revolution-as-parcel-demand-soars-idUSKBN1DA0RN")
    urls20.append("http://www.reuters.com/article/us-music-ema/shawn-mendes-eminem-and-u2-among-winners-at-mtv-europe-music-awards-idUSKBN1DC13Q")
    urls20.append("http://www.reuters.com/article/us-southkorea-china-entertainment/south-korea-celebrity-appears-in-chinese-ad-in-subtle-sign-of-thawing-diplomatic-tension-idUSKBN1DD14H")
    urls20.append("http://www.reuters.com/article/us-science-pyramid-virtualreality/exploring-egypts-great-pyramid-from-the-inside-virtually-idUSKBN1D72UB")
    urls20.append("http://www.reuters.com/article/us-science-footprints/fossil-footprints-reveal-existence-of-big-early-dinosaur-predator-idUSKBN1CV3EE")
    urls20.append("http://www.reuters.com/article/us-trump-effect-coal-revival/a-year-after-trumps-election-coals-future-remains-bleak-idUSKBN1DD0IA")
    urls20.append("http://www.reuters.com/article/us-britain-politics-breakingviews/breakingviews-uk-economy-will-share-theresa-mays-pain-idUSKBN1DD1JU")
    parteC = ParteC(urls20)
    parteC.exe()