import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle
#nltk.download('punkt')
def preProcess(doc):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(doc)
    Tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [stemmer.stem(word) for word in words]
        words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]
        
        words = [word for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords
        #words= [word for word in words if word.isalnum() and word not in Stopwords]
        Tokens.extend(words)
        
    return ' '.join(Tokens)
with open("articlesData.data", "rb") as f:
    articlesData = pickle.load(f)
preProcessedArticlesData = []
for a in articlesData:
    prepArticle = {}
    prepArticle['monthInd'] = a["monthInd"]
    prepArticle['title'] = preProcess(a["title"])
    prepArticle['abstract'] = preProcess(a["abstract"])
    prepArticle['authorTags'] = [preProcess(x) for x in a["authorTags"]]
    prepArticle['ccsClass'] = [preProcess(x) for x in a["ccsClass"]]
    preProcessedArticlesData.append(prepArticle)
with open("preProcessedArticlesData.data", "wb") as f:
    pickle.dump(preProcessedArticlesData, f)