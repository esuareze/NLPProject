import pickle

with open("cleanArticlesData.data", "rb") as f:
    articles = pickle.load(f)
concepts = []
for a in articles:
    concepts.extend(a['ccsClass'])
concepts = [c.lower() for c in concepts if c != '']
concepts = set(concepts)
with open("QuickData/concepts.data", "wb") as f:
    pickle.dump(concepts, f)
while True:
    Q = input("pls halp: ").lower()
    for con in concepts:
        if con in Q:
            print("efe")
