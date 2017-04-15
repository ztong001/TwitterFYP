"""Sentiment lexicon extension codes"""
# import csv
from functools import reduce
from inspect import getsourcefile
from itertools import chain
from os.path import abspath, dirname, join

from nltk.corpus import stopwords, wordnet
from nltk.sentiment.vader import BOOSTER_DICT, NEGATE
from nltk.tokenize import TweetTokenizer

# from evaluation import get_dataset


class LexiconEnhancer(object):
    """
    Class for expanding the lexicon based on incoming words
    new_words: Set of new words obtained from corpus
    new_word tuple: (word, pos_score, neg_score)
    """

    def __init__(self, lexicon_file="vader_lexicon.txt"):
        self.new_words = []
        self.lex_dict = {}
        lexicon_full_filepath = join(
            dirname(abspath(getsourcefile(lambda: 0))), lexicon_file)
        with open(lexicon_full_filepath) as fp:
            self.lexicon_filepath = fp.read()
        for line in self.lexicon_filepath.split('\n'):
            (word, measure) = line.strip().split('\t')[0:2]
            self.lex_dict[word] = float(measure)

    def write_word_to_lexicon(self, lexicon_file):
        """
        Similar to write_to_lexicon(), with difference that it writes the new word and scores
        back to the file directly
        """
        lexicon_full_filepath = join(
            dirname(abspath(getsourcefile(lambda: 0))), lexicon_file)
        with open(lexicon_full_filepath, mode='a') as fp:
            for word in self.new_words:
                fp.write("{}\t{}\t{}\n".format(
                    word[0], word[1], word[2]))

    def mine_candidates(self, corpus):
        """
        Detect potential new words in the corpus(list of tokens)
        """
        tokenizer = TweetTokenizer()
        tokens_corpus = [tokenizer.tokenize(entry) for entry in corpus]
        known_words = [chain(stopwords.words(
            'english')), NEGATE, list(BOOSTER_DICT.keys()), list(self.lex_dict.keys())]
        unique_words = set(chain.from_iterable(tokens_corpus))
        candidates = [
            word.lower() for word in unique_words if word not in known_words and word.isdigit() is False and len(word) > 1]
        return candidates

    @staticmethod
    def evaluate_candidates(correlated):
        """
        Check if candidate word fulfils criteria of having lexicon words in its context
        More than or equal to 3 -> new_words and surrounding words
        """
        return len(correlated) >= 3

    def find_correlated(self, corpus, new_word):
        """
        Find correlated words for a single new word
        returns List correlated, where index 0 is the word itself
        """
        lexicon_words = list(self.lex_dict.keys())
        correlated = [new_word]
        for sentence in corpus:
            if new_word in sentence and sentence.index(new_word) in range(1, len(sentence) - 1):
                w_index = sentence.index(new_word)
                if set(lexicon_words) & set(sentence[0:w_index]) != []:
                    co_left = set(lexicon_words).intersection(
                        set(sentence[0:w_index]))
                if set(lexicon_words) & set(sentence[w_index:]) != []:
                    co_right = set(lexicon_words).intersection(
                        set(sentence[w_index:]))
                correlated.extend([co_left, co_right])
        return correlated

    def evaluate_sentiment(self, new_word, n_gram):
        """
        Analyse sentiment of new word based on co-occurence words
        1) calculate similarity between old words and new word (2 old words to 1 new words eg)
        2) normalized similarity weightage * score of old words to find new word score
        3) Do it for both positive and negative score lexicon
        """
        print(new_word)
        print(n_gram)
        lexicon = self.lex_dict
        word_scores = {word: lexicon[word]
                       for word in n_gram if word in lexicon}
        print(word_scores)
        # get similarity of word against new word, save as
        # word_scores[word][2]
        for word in word_scores:
            word_scores[word].append(
                wordnet.wup_similarity(new_word, word))
            print(word, word_scores[word])
        similarity_total = sum([word[2] for word in word_scores])
        # word[0] is positive score, word[1] is negative score
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

# if __name__ == "__main__":

#     dataset = get_dataset('preprocessed.csv')
#     tweets = [item[0] for item in dataset]
#     enhancer = LexiconEnhancer()

#     c_words = enhancer.mine_candidates(tweets)
#     print("Mining complete: {} candidate words".format(len(c_words)))
#     n_grams_set = []
#     for w in c_words:
#         n_grams = enhancer.find_correlated(tweets, w)
#         if enhancer.evaluate_candidates(n_grams):
#             n_grams_set.append(n_grams)
#     wordpath = join(
#         dirname(abspath(getsourcefile(lambda: 0))), "wordlist.txt")
#     print("Writing to file")
#     with open(wordpath, 'w', encoding='utf8') as wordlist:
#         for w in c_words:
#             wordlist.write(w + '\n')
