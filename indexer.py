import gensim
import numpy as np
import pickle
import math


print("loading model...")
#The same as an imported trained Vec2Word model but now its called KeyedVectors
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

print("model loaded.")

TITLE_FRAC = 5
ABSTRACT_FRAC = 2
KEYWORDS_FRAC = 5 # it is then multiplied by the log base 2 of the amound of keywords useable +1

def text2Vec(text):
    words = text.split(" ")
    vectors = [model.get_vector(w) for w in words if model.has_index_for(w)]
    if len(vectors) == 0:
        return None
    result = np.average(vectors, axis = 0)
    return result

def calculate_index(article):
    total = TITLE_FRAC
    title_vec = text2Vec(article['title'])
    total_vec = title_vec*TITLE_FRAC
    if article['abstract'] != "":
        total +=ABSTRACT_FRAC
        abstract_vec = text2Vec(article['abstract'])*ABSTRACT_FRAC
        total_vec = [total_vec[i] + abstract_vec[i] for i in range(len(total_vec))]
    keywords = article['authorTags']
    if len(keywords) > 0:
        usable_keywords = 0
        kw_vecs = []
        for kw in keywords:
            vec = text2Vec(kw)
            if vec is not None:
                usable_keywords +=1
                kw_vecs.append(vec)
        if usable_keywords > 0:
            adjusted_kw_frac = KEYWORDS_FRAC*math.log(usable_keywords+1, 2)
            total += adjusted_kw_frac
            kw_np = np.asarray(kw_vecs)
            kw_vec = np.average(kw_vecs, axis = 0)
            kw_vec = kw_vec * adjusted_kw_frac
            total_vec = [total_vec[i] + kw_vec[i] for i in range(len(total_vec))]
    total_vec = [x / total for x in total_vec]
    return total_vec

with open("cleanArticlesData.data", "rb") as f:
    articles = pickle.load(f)
search_info = [] #list of search information of all articles. Search information is the feature vector (len 300) and list of ccs categories and its index on the original list.
print("calculating vectors...")
for i, a in enumerate(articles):
    search_info.append((calculate_index(a), a['ccsClass'], i))
print("saving data...")
with open("index.data", "wb") as f:
    pickle.dump(search_info, f)
print("Done.")
"""
for s in search_info:
    print(f"vector: {s[0]}")
    print(f"concepts: {s[1]}")
    print("-----------------------------")
"""