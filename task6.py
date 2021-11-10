
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn


def stem_lem(words):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    words = [stemmer.stem(word) for word in words]
    words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]
        
    return words

def augment(wordList):
    result = []
    for w in wordList:
        for s in wn.synsets(w):
            result.append(s.name().split(".")[0])
        result.append(w)
    return list(set(result))

import pickle
import numpy as np

with open("cleanArticlesData.data", "rb") as f:
    articlesData = pickle.load(f)

numMonths = articlesData[-1]["monthInd"]+1
numTopConcepts = 5

#dictionary where the keys are the keywird/author tags and the value is a list containing every month they have been mentioned in. len(keywordMonths["kw"]) = number of times the keyword "kw" has been used. Values of the list are simply the month it has been used in
keywordMonths = {}
for a in articlesData:
    for kw in a["ccsClass"]:
        kw = kw.lower()
        if kw in keywordMonths.keys():
            keywordMonths[kw].append(a)
        else:
            keywordMonths[kw] = [a]
topConcepts = sorted(keywordMonths.items(), reverse=True, key=lambda tup: len(tup[1]))[:numTopConcepts]
topConcepts = {c:a for c,a in topConcepts}





topConceptsWithKw = {}

results = {}

for key in topConcepts.keys():
    topConceptsWithKw[key] = [x for x in topConcepts[key] if len(x['authorTags'])>0]
    results[key] = {}
    results[key]['pWithKw'] = len(topConceptsWithKw[key]) / len(topConcepts[key])


for key, value in topConceptsWithKw.items():
    pTitleInKw = []
    pKwInTitle = []
    totalTitleWords = 0
    totalKwWords = 0
    totalTitleWordsInKw = 0
    totalKwWordsInTitle = 0
    for a in value:
        titleWords = a['title'].split(" ")
        titleWordsAug = augment(titleWords)
        titleWordsAug = stem_lem(titleWords)
        kwWords = []
        for kw in a['authorTags']:
            kwWords.extend(kw.split(" "))
        kwWords = stem_lem(kwWords)
        titleWordsInKw = [x for x in titleWords if x in kwWords]
        kwWordsInTitle = [x for x in kwWords if x in titleWordsAug]
        pTitleInKw.append(len(titleWordsInKw) / len(titleWords))
        pKwInTitle.append(len(kwWordsInTitle) / len(kwWords))
        totalTitleWords +=len(titleWords)
        totalKwWords += len(kwWords)
        totalTitleWordsInKw += len(titleWordsInKw)
        totalKwWordsInTitle += len(kwWordsInTitle)
    results[key] = {}
    results[key]['avgPTitleInKw'] = np.average(pTitleInKw)
    results[key]['avgPKwInTitle'] = np.average(pKwInTitle)
    results[key]['totalPTitleInKw'] = totalTitleWordsInKw / totalTitleWords
    results[key]['totalPKwInTitle'] = totalKwWordsInTitle / totalKwWords
    results[key]['pArticlesWithKw'] = len(topConceptsWithKw[key])/len(topConcepts[key])
for key,value in results.items():
    
    print(key)
    for k,v in results[key].items():
        print(f"{k} : {v}")
    print("---------------")
with open("QuickData/KwToTitleAugmented.data", "wb") as f:
    pickle.dump(results, f)
