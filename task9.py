from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import gensim
from scipy.spatial.distance import cosine
from inspect import signature
print(signature(gensim.models.Word2Vec.load))
import numpy as np
import pickle
with open("cleanArticlesData.data","rb") as f:
    articles = pickle.load(f)
for a in articles:
    newTags = []
    for kw in a['authorTags']:
        newTags.extend(kw.split(" "))
    a['authorTags'] = newTags
#The same as an imported trained Vec2Word model but now its called KeyedVectors
model = gensim.models.KeyedVectors.load_word2vec_format('I:\\NLP\\Project\\GoogleNews-vectors-negative300.bin.gz', binary=True)

#only articles with both abstract and keywords        
filteredArticles = [a for a in articles if (a['abstract'] != "" and  len(a['authorTags']) > 0)]

#generates a vector from a text by averaging the vectors for each word
def text2Vec(text):
    words = text.split(" ")
    vectors = [model.get_vector(w) for w in words if model.has_index_for(w)]
    result = np.average(vectors, axis = 0)
    return result

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
        overlap = []
        abstract_vec = text2Vec(a['abstract'])
        title_vec = text2Vec(a['title'])
        abstract_title_vec = [(abstract_vec[i]+title_vec[i])/2 for i in range(len(title_vec))]
        for kw in a['authorTags']:
            if model.has_index_for(kw):
                overlap.append(cosine(model.get_vector(kw), abstract_title_vec))
        if (len(overlap) != 0):
            overlappings[ccs].append(sum(overlap)/len(overlap))
result = {}
for key, value in overlappings.items():
    result[key] = sum(value)/len(value)

#por cada ccs, media de los overlappings de todos sus articulos
with open("QuickData/vec2wordoverlapping2", "wb") as f:
    pickle.dump(result, f)
#por cada ccs, lista de los overlappings de sus articulos
with open("QuickData/vec2wordoverlapping2raw", "wb") as f:
    pickle.dump(overlappings, f)
