"""Sentiment lexicon extension codes"""
from functools import reduce
from inspect import getsourcefile
from itertools import chain
from os.path import abspath, dirname, join

from nltk.corpus import stopwords, wordnet, words
from nltk.util import ngrams


def add_to_lexicon(lexicon, new_word, score):
    """
    Add new word and its sentiment score to lexicon
    """
    lexicon[new_word] = score


def write_word_to_lexicon(new_word, score, lexicon_file):
    """
    Similar to write_to_lexicon(), with difference that it writes the new word and scores
    back to the file directly
    """
    lexicon_full_filepath = join(
        dirname(abspath(getsourcefile(lambda: 0))), lexicon_file)
    with open(lexicon_full_filepath, mode='a') as fp:
        fp.write("{}\t{}\t{}\n".format(new_word, score[0], score[1]))


def evaluate_sentiment(new_word, sentence, lexicon):
    """
    Analyse sentiment of new word based on co-occurence words
    1) get sentence, find n-grams with new word (co-occurence)
    2) calculate similarity between old words and new word (2 old words to 1 new words eg)
    3) normalized similarity weightage * score of old words to find new word score
    4) Do it for both positive and negative score lexicon
    """
    stop_words = set(stopwords.words('english'))
    if new_word in stop_words:
        return [0, 0]
    else:
        new_word_gram = [gram for gram in ngrams(
            sentence, 3) if new_word in gram]
        new_word_gram = set(chain.from_iterable(new_word_gram))
        print(new_word_gram)
        word_scores = {word: lexicon[word]
                       for word in new_word_gram if word in lexicon}
        print(word_scores)
        # get similarity of word against new word, save as word_scores[word][2]
        for word in word_scores:
            word_scores[word].append(wordnet.wup_similarity(new_word, word))
            print(word, word_scores[word])
        similarity_total = sum([word[2] for word in word_scores])
        pos_score = reduce((lambda x, y: x * y),
                           ((word[0], word[2]) for word in word_scores)) / similarity_total
        neg_score = reduce((lambda x, y: x * y),
                           ((word[1], word[2]) for word in word_scores)) / similarity_total
        return [pos_score, neg_score]


def label_sentiment(scores):
    """
    Returns the sentiment label pos/neu/neg for the tweet
    """
    main_score = scores.get('compound')
    if main_score > 0.1:
        return 'pos'
    elif main_score < -0.1:
        return 'neg'
    else:
        return 'neu'
