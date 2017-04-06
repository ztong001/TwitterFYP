"""Sentiment lexicon extension codes"""
from inspect import getsourcefile
from os.path import abspath, join, dirname
from nltk.tag.perceptron import PerceptronTagger
from nltk.corpus import stopwords


def add_to_lexicon(lexicon, new_word, score):
    """
    Add new word and its sentiment score to lexicon
    """
    lexicon[new_word] = score


def write_to_lexicon(lexicon, lexicon_file):
    """
    Convert lexicon dictionary back to txt file
    """
    lexicon_full_filepath = join(
        dirname(abspath(getsourcefile(lambda: 0))), lexicon_file)
    with open(lexicon_full_filepath, mode='w') as fp:
        for line in lexicon:
            fp.write("{}\t{}\n".format(line, lexicon[line]))


def write_word_to_lexicon(new_word, score, lexicon_file):
    """
    Similar to write_to_lexicon(), with difference that it writes the new word and scores
    back to the file directly
    """
    lexicon_full_filepath = join(
        dirname(abspath(getsourcefile(lambda: 0))), lexicon_file)
    with open(lexicon_full_filepath, mode='a') as fp:
        fp.write("{}\t{}\n".format(new_word, score))


def evaluate_sentiment(new_word, sentence):
    """
    Analyse sentiment of new word based on word vector or surrounding context
    1) get sentence, POS tag it, get the word's POStag to identify its word type
    2) get word vector, find similarity with other words in lexicon
    """
    if new_word in set(stopwords):
        return
    pos_tagger = PerceptronTagger()
    new_word_pos = dict(pos_tagger.tag(sentence)).get(new_word)

    return score
