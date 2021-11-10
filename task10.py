import gensim
import numpy as np
import pickle
from scipy.spatial.distance import cosine
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

def text2Vec(text):
    words = text.split(" ")
    vectors = [model.get_vector(w) for w in words if model.has_index_for(w)]
    if len(vectors) == 0:
        return None
    result = np.average(vectors, axis = 0)
    return result
def preProcess(doc):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))

    sentences = sent_tokenize(doc)
    Tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        #words = [stemmer.stem(word) for word in words]
        #words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]
        
        words = [word for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords
        #words= [word for word in words if word.isalnum() and word not in Stopwords]
        Tokens.extend(words)
        
    return ' '.join(Tokens)

def has_concept(article_concepts, concepts_to_check):
    for con in article_concepts:
        if con.lower() in concepts_to_check:
            return True
    return False

NUMBER_OF_RESULTS = 3

print("loading model...")
#The same as an imported trained Vec2Word model but now its called KeyedVectors
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
with open("index.data", "rb") as f:
    search_info = pickle.load(f)
#its already in lower case
with open("QuickData/concepts.data", "rb") as f:
    possible_concepts = pickle.load(f)
with open("articlesData.data","rb") as f:
    articles = pickle.load(f)
print("model loaded.")
while True:
    #get query and preprocess (and convert to vector)
    Q = input("Insert your query:").lower()

    Q = preProcess(Q)
    Q_vec = text2Vec(Q)
    if Q_vec is None:
        print("Unfortunately the query only contains unknown words. Please try again using common english words.")
        continue
    #get any concept that may have been searched and filter articles that have said concept (if it has any)
    concepts_contained = []
    for con in possible_concepts:
        if con in Q:
            concepts_contained.append(con)
    if len(concepts_contained) > 0:
        search_space = [s for s in search_info if has_concept(s[1], concepts_contained)]
    else:
        search_space = search_info
    #now to compare articles' similarity to query
    similitudes = [(cosine(Q_vec,s[0]), s[2]) for s in search_space] # for each article, save similitud (cosine) and its index (to later get its full info)
    top_similitudes = sorted(similitudes,reverse=True, key = lambda x:x[0])[:NUMBER_OF_RESULTS]
    #get and print info about results
    for i, result in enumerate(top_similitudes):
        a = articles[result[1]]
        print(f"RESULT {i+1} --------------------")
        print(f"TITLE: {a['title']}")
        print(f"ABSTRACT: {a['abstract'] if a['abstract']!= '' else 'No Abstract Available' }")
        print(f"CONCEPTS: {a['ccsClass'] if len(a['ccsClass'])>0 else 'No Concepts Available' }")
        print(f"KEYWORDS: {a['authorTags'] if len(a['authorTags'])>0 else 'No Keywords Available' }")
        print(f"MONTH: {a['monthInd']}")