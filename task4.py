import pickle
with open("articlesData.data","rb") as f:
    articles = pickle.load(f)

numMonths = articles[-1]["monthInd"]+1
numTopConcepts = 5

#dictionary where the keys are the keywird/author tags and the value is a list containing every month they have been mentioned in. len(keywordMonths["kw"]) = number of times the keyword "kw" has been used. Values of the list are simply the month it has been used in
conceptMonths = {}
for a in articles:
    for ccs in a["ccsClass"]:
        ccs = ccs.lower()
        if ccs in conceptMonths.keys():
            conceptMonths[ccs].append(a["monthInd"])
        else:
            conceptMonths[ccs] = [a["monthInd"]]
topConcepts = sorted(conceptMonths.items(), reverse=True, key=lambda tup: len(tup[1]))[:numTopConcepts]
for w in topConcepts:
    print(f"{w[0]} : {len(w[1])}")
topConceptCounts = {}

for w in topConcepts:
    keyword = w[0]
    months = w[1]
    topConceptCounts[keyword] = [0]*numMonths
    for m in months:
        topConceptCounts[keyword][m]+=1
for aw in topConceptCounts.keys():
    print(aw, end="")
    print(topConceptCounts[aw])
    print(sum(topConceptCounts[aw]))
#topKwCounts is a dictionary where keys are the top 10 most used keywords and the values are lists of length numMonths where every value of the list is the times that keyword was used that month

with open("QuickData/topConceptCounts","wb") as f:
    pickle.dump(topConceptCounts, f)