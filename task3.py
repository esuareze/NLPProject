import pickle
with open("articlesData.data","rb") as f:
    articles = pickle.load(f)

numMonths = articles[-1]["monthInd"]+1
numTopKeywords = 10

#dictionary where the keys are the keywird/author tags and the value is a list containing every month they have been mentioned in. len(keywordMonths["kw"]) = number of times the keyword "kw" has been used. Values of the list are simply the month it has been used in
keywordMonths = {}
for a in articles:
    for kw in a["authorTags"]:
        kw = kw.lower()
        if kw in keywordMonths.keys():
            keywordMonths[kw].append(a["monthInd"])
        else:
            keywordMonths[kw] = [a["monthInd"]]
topKeywords = sorted(keywordMonths.items(), reverse=True, key=lambda tup: len(tup[1]))[:numTopKeywords]
for w in topKeywords:
    print(f"{w[0]} : {len(w[1])}")
topKwCounts = {}

for w in topKeywords:
    keyword = w[0]
    months = w[1]
    topKwCounts[keyword] = [0]*numMonths
    for m in months:
        topKwCounts[keyword][m]+=1
for aw in topKwCounts.keys():
    print(aw, end="")
    print(topKwCounts[aw])
    print(sum(topKwCounts[aw]))
#topKwCounts is a dictionary where keys are the top 10 most used keywords and the values are lists of length numMonths where every value of the list is the times that keyword was used that month

with open("QuickData/topKwCounts","wb") as f:
    pickle.dump(topKwCounts, f)