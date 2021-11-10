# NLPProject
## Requirements

All the packages contained in the environment used to run the project are listed in requirements.txt

##Project Structure

### Programs

Code for tasks 1-10 is available in files task<n>.py where <n> is the number of the task. Additionally, task<n>Vis.ipynb holds the jupyter notebook code to visualize any graph necessary for the task.

Other code files:

	* indexer.py : generates the index.data by vectorizing every article and saving the vector along with that article's index in the original list and its ccs concepts.

	* Keyword Usage Per Month.ipynb : visualizes both the raw amount of keywords used in every month (in our data-set) and the amount of articles that had at least one keyword for each month (in our data-set).

	* possibleConcepts.py : makes a list with all existing ccs concepts in the data-set and saves it to QuickData/concepts.data

	* preProcess.py : has been used to make both cleanArticlesData.data and preProcessedArticlesData.data . Both functionalities can be achieved with the same program changing the preProcess function.

### Data

Data is separated in 2 large groups. The first one is in the main folder and contains the main data-set, versions of it and its index. The second group is small data files that are the result of processing the main data-set to gather metrics. This second group is saved in the QuickData folder. All data has been saved using pickle. Data files:

	* articlesData.data : data of all the articles scrapped. Abstract has been modified to be an empty string when there is no abstract available. Its a list of dictionaries. Each dictionary represents an article and has : 'monthInd', 'title', 'abstract', 'authorTags' and 'ccsClass'.

	* cleanArticlesData.data : same as articlesData.data but every stopword, numbers and punctuation has been removed from texts.

	* preProcessedArticlesData.data : same as cleanArticlesData.data but every word from all texts (including keywords and concepts) has been lemmatized and stemmed.

	* index.data : for each article contains its vector, its ccs concepts and its index.

	* concepts.data : list of all existing ccs concepts in the data-set.

	* kwToTitle.data : all types of overlappings calculated with string matching between keywords and titles for articles in the top 5 most used CCS Concepts and separated each in its CCS Concept.

	* kwToTitleAugmented.data : all types of overlappings calculated with string matching between keywords and augmented titles (augmented using synonyms) for articles in the top 5 most used CCS Concepts and separated each in its CCS Concept.

	* num_results : for each month number of search results of articles.

	* tfidfoverlapping : for each ccs concept, average amount of overlapping between its articles' abstracts and keywords using tf-idf method.

	* tfidfoverlappingraw : for each ccs concept, list of amount of overlapping between its articles' abstracts and keywords using tf-idf method for each article in it.

	* topConceptCounts : for the top 5 most used ccs concepts, a list containing the amount of articles in said concept for each month.

	* topKwCounts : for the top 10 most used keywords, a list containing the amount of articles using said keyword for each month.

	* vec2wordoverlapping1 : for each ccs concept, average amount of overlapping between its articles' abstracts and keywords using word2Vec method.

	* vec2wordoverlapping1raw : for each ccs concept, list of amount of overlapping between its articles' abstracts and keywords using word2Vec method for each article in it.

	* vec2wordoverlapping2 : for each ccs concept, average amount of overlapping between its articles' abstracts and titles, and keywords using word2Vec method.

	* vec2wordoverlapping2raw : for each ccs concept, list of amount of overlapping between its articles' abstracts and title, and keywords using word2Vec method for each article in it.