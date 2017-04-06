"""Feature extraction with Bag-of-Words, then use MultinomialNB"""
import sqlite3
import logging
from inspect import getsourcefile
from os.path import abspath, join, dirname
import sys
import collections
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify.util import accuracy
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from evaluation import generate_eval_metrics, class_list
from features import bag_of_words


log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


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

    DB_PATH = join(dirname(abspath(getsourcefile(lambda: 0))), "outdata.db")
    data = getdata_from_db(DB_PATH)
    label_feats = label_feats_from_data(data)
    train_feats, test_feats = train_test_split(
        label_feats, train_size=0.7, test_size=0.3)
    mnb_classify = SklearnClassifier(MultinomialNB())
    mnb_classify.train(train_feats)


if __name__ == "__main__":
    mnb_classifier()
