"""Feature extraction using word vectors, then use LinearSVC"""
import csv
import logging
import sqlite3
import sys
from inspect import getsourcefile
from os.path import abspath, dirname, join

import numpy as np
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from gensim.utils import tokenize
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import Imputer, label_binarize
from sklearn.svm import LinearSVC

from evaluation import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def makeFeatureVec(list_word, model, num_features):
    """
    Averages the word vectors for a sentence
    """
    feature_vector = np.zeros((num_features,), dtype="float32")
    index2word_set = set(model.index2word)
    # check if in model's vocab, add vector to total
    nwords = 0
    for word in list_word:
        if word in index2word_set:
            nwords += 1.
            feature_vector = np.add(feature_vector, model[word])

    # Divide the result by the number of words to get the average
    feature_vector = np.divide(feature_vector, nwords)
    return feature_vector


def getAvgFeatureVecs(sentence_list, model, num_features):
    """
    Calculate average feature vector for each sentence
    """
    av_vector_list = np.zeros(
        (len(sentence_list), num_features), dtype="float32")
    counter = 0
    for review in sentence_list:
        if counter % 50. == 0:
            print("Sentence %d of %d" % (counter, len(sentence_list)))
        av_vector_list[counter] = makeFeatureVec(review, model, num_features)
        counter += 1
    return av_vector_list


def word2vec_classifier(dataset):
    documents = []
    for line in dataset:
        # Wrapper method for tokenizing with
        tokens = tokenize(line[0], lower=True)
        sentence = LabeledSentence(tokens, line[1])
        documents.append(sentence)
    log.info("Doc2Vec %d lines" % (len(documents)))
    # Model parameters
    num_features = 100
    min_word_count = 1
    num_workers = 8
    context = 2
    downsampling = 1e-3
    d2v_model = Doc2Vec(min_count=min_word_count, window=context, size=num_features,
                        sample=downsampling, workers=num_workers)
    log.info("Training doc vectors")
    train_set, test_set = train_test_split(
        documents, train_size=0.7, test_size=0.3)
    train_vec = getAvgFeatureVecs(train_set, d2v_model, num_features)
    test_vec = getAvgFeatureVecs(test_set, d2v_model, num_features)
    train_vec = Imputer().fit_transform(train_vec)
    test_vec = Imputer().fit_transform(test_vec)

    # train model and predict with LinearSVC
    model = LinearSVC()
    classifier_fitted = OneVsRestClassifier(model).fit(train_vec, train_set[1])
    result = classifier_fitted.predict(test_vec)

    # output result to csv
    result.tofile("./d2v_linsvc.csv", sep='\t')

    # store the model to mmap-able files
    joblib.dump(model, 'model/%s.pkl' % 'd2v_linsvc')

    # evaluation
    label_score = classifier_fitted.decision_function(test_vec)
    binarise_result = label_binarize(result, classes=class_list)
    binarise_labels = label_binarize(class_list, classes=class_list)

    # generate_eval_metrics(binarise_result, 'w2v_linsvc', binarise_labels)
    generate_report(binarise_result, 'w2v_linsvc', binarise_labels)

if __name__ == "__main__":
    dataset = get_dataset("preprocessed.csv")
    word2vec_classifier(dataset)
