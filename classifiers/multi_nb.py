"""Feature extraction with Bag-of-Words, then use MultinomialNB"""
import sqlite3
import logging
import os
import sys
import collections
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify.util import accuracy
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from features import bag_of_words, bag_of_non_stopwords
# >>> from nltk.corpus import movie_reviews
# >>> from featx import label_feats_from_corpus, split_label_feats
# >>> movie_reviews.categories()
# ['neg', 'pos']
# >>> lfeats = label_feats_from_corpus(movie_reviews)
# >>> lfeats.keys()
# dict_keys(['neg', 'pos'])
# >>> train_feats, test_feats = split_label_feats(lfeats)
# >>> len(train_feats)
# 1500
# >>> len(test_feats)
# 500

log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

FILE_DIR = os.path.dirname(os.path.realpath('__file__'))
print(FILE_DIR)


def getdata_from_db(database_path, number='max'):
    """Select labelled data from the database"""
    connect = sqlite3.connect(database_path)
    log.info("Connecting to database")
    query = connect.cursor()
    if number == 'max':
        query.execute("SELECT text,label FROM labels ORDER BY id; ")
    else:
        query.execute(
            "SELECT text,label FROM labels ORDER BY id DESC LIMIT " + str(number) + "; ")
    for line in query.fetchall():
        tweets = [].append((line[0], line[1]))
    log.debug("Tweets from databases: %d tweets" % (len(tweets)))
    return tweets


def label_feats_from_data(data, feature_detector=bag_of_words):
    label_feats = collections.defaultdict(list)

    for label in data[1]:
        feats = feature_detector(data[0])
        label_feats[label].append(feats)
    return label_feats


def mnb_classifier():
    DB_PATH = os.path.join(FILE_DIR, 'db/outdata.db')
    print(DB_PATH)
    data = getdata_from_db(DB_PATH)
    label_feats = label_feats_from_data(data)
    train_feats, test_feats = train_test_split(
        label_feats, train_size=0.7, test_size=0.3)
    mnb_classify = SklearnClassifier(MultinomialNB())
    mnb_classify.train(train_feats)
    print(accuracy(mnb_classify, test_feats))

if __name__ == "__main__":
    mnb_classifier()
