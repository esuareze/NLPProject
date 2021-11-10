from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import pickle

import pickle
with open("preProcessedArticlesData.data","rb") as f:
    articles = pickle.load(f)
filteredArticles = [a for a in articles if (a['abstract'] != "" and  len(a['authorTags']) > 0)]

articlesByCcs = {}
for a in filteredArticles:
    for ccs in a["ccsClass"]:
        ccs = ccs.lower()
        if ccs in articlesByCcs.keys():
            articlesByCcs[ccs].append(a)
        else:
            articlesByCcs[ccs] = [a]
overlappings = {}
for ccs in articlesByCcs.keys():
    overlappings[ccs] = []
    for a in articlesByCcs[ccs]:
        transformer = TfidfVectorizer()
        transformer.fit([a['abstract']])
        overlap = []
        for kw in a['authorTags']:
            kwTfIdf = transformer.transform([kw]).toarray()[0]
            overlap.append(sum(kwTfIdf))
        overlappings[ccs].append(sum(overlap)/len(overlap))
result = {}
for key, value in overlappings.items():
    result[key] = sum(value)/len(value)
#por cada ccs, media de los overlappings de todos sus articulos
with open("QuickData/tfidfoverlapping", "wb") as f:
    pickle.dump(result, f)
#por cada ccs, lista de los overlappings de sus articulos
with open("QuickData/tfidfoverlappingraw", "wb") as f:
    pickle.dump(overlappings, f)
