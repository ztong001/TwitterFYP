import logging
from pprint import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
categories = ['pos', 'neg', 'neu']
# Uncomment the following to do the analysis on all the categories
#categories = None

print("Loading twitter dataset for categories:")
print(categories)
# TODO: Load data into data.data and data.target
print()

pipeline = Pipeline([
    ('tfidfvect', TfidfVectorizer()),
    ('mnb', MultinomialNB())
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'tfidfvect__max_df': (0.5, 0.75, 1.0),
    #'vect__max_features': (None, 5000, 10000, 50000),
    'tfidfvect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    'tfidfvect__use_idf': True,
    'tfidfvect__norm': ('l1', 'l2'),
    'mnb__alpha': (0.00001, 0.000001),
    #'clf__n_iter': (10, 50, 80),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(data.data, data.target)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
