import pickle
import numpy as np


with open("preProcessedArticlesData.data", "rb") as f:
    articlesData = pickle.load(f)


numMonths = articlesData[-1]["monthInd"]+1
numTopConcepts = 5

#dictionary where the keys are the keywird/author tags and the value is a list containing every month they have been mentioned in. len(keywordMonths["kw"]) = number of times the keyword "kw" has been used. Values of the list are simply the month it has been used in
articlesPerConcept = {}
for a in articlesData:
    for ccs in a["ccsClass"]:
        ccs = ccs.lower()
        if ccs in articlesPerConcept.keys():
            articlesPerConcept[ccs].append(a)
        else:
            articlesPerConcept[ccs] = [a]
topConcepts = sorted(articlesPerConcept.items(), reverse=True, key=lambda tup: len(tup[1]))[:numTopConcepts]
topConcepts = {c:a for c,a in topConcepts}

topConceptsWithKw = {}

results = {}

for key in topConcepts.keys():
    topConceptsWithKw[key] = [x for x in topConcepts[key] if len(x['authorTags'])>0]


for key, value in topConceptsWithKw.items():
    pTitleInKw = []
    pKwInTitle = []
    totalTitleWords = 0
    totalKwWords = 0
    totalTitleWordsInKw = 0
    totalKwWordsInTitle = 0
    for a in value:
        titleWords = a['title'].split(" ")
        kwWords = []
        for kw in a['authorTags']:
            kwWords.extend(kw.split(" "))
        titleWordsInKw = [x for x in titleWords if x in kwWords]
        kwWordsInTitle = [x for x in kwWords if x in titleWords]
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
with open("QuickData/KwToTitle.data", "wb") as f:
    pickle.dump(results, f)
