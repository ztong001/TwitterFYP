"""Feature extraction with Bag-of-Words, then use MultinomialNB"""

import logging
import sys
import collections
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from evaluation import *
from features import bag_of_non_stopwords


log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def label_feats_from_data(data, feature_detector):
    label_feats = collections.defaultdict(list)
    for label in data[1]:
        feats = feature_detector(data[0])
        label_feats[label].append(feats)
    return label_feats


def mnb_classifier(dataset):

    label_feats = label_feats_from_data(dataset, bag_of_non_stopwords)
    train_feats, test_feats = train_test_split(
        label_feats, train_size=0.7, test_size=0.3)
    mnb_classify = SklearnClassifier(MultinomialNB())
    mnb_classify.train(train_feats)
    result = mnb_classify.classify(test_feats)

    generate_report(result, 'bow_mnb', class_list)


if __name__ == "__main__":
    data_set = get_dataset("preprocessed.csv")
    mnb_classifier(data_set)
