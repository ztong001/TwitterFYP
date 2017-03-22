# encoding: utf-8
"""preprocessing procedure with POS tagging and tokenisation"""
import json
import os
import sqlite3
import string

from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import preprocessor as pre
from bs4 import BeautifulSoup
from replacer import ComboReplacer
from vader_tagging import getlabel, save_data_to_db
from setup import *

with open(CONFIG_PATH) as f:
    config = json.load(f)

lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer(
    strip_handles=True, preserve_case=False, reduce_len=True)
outfile = os.path.join(ROOT_DIR, "outData/preprocessed.txt")
replacer = ComboReplacer()
# Filter out URLs, mentions, hashtags and emojis
pre.set_options(pre.OPT.URL, pre.OPT.MENTION,
                pre.OPT.HASHTAG, pre.OPT.EMOJI)


def lemmatize(token, tag):
    tag = {
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV,
        'J': wordnet.ADJ
    }.get(tag[0], wordnet.NOUN)

    return lemmatizer.lemmatize(token, tag)


def preprocess(sentence, stop_words, lemma=True):
    """Function to clean, tokenise and preprocess a tweet with tweet-preprocessor"""
    cleaned_string = pre.clean(sentence)
    cleaned_string = BeautifulSoup(cleaned_string, "html.parser").get_text()
    replaced_string = replacer.replaceAll(cleaned_string)
    tokens = tokenizer.tokenize(replaced_string)
    preprocessed_string = []
    for token, tag in pos_tag(tokens):
        # If stopword, ignore token and continue
        if token in stop_words:
            continue
        # If punctuation, ignore token and continue
        if all(char in string.punctuation for char in token):
            continue
        # Lemmatize the token
        if lemma:
            token = lemmatize(token, tag)
        preprocessed_string.append(token)
    tokens = [s.translate(str.maketrans('', '', string.punctuation))
              for s in preprocessed_string]
    tokens = " ".join(tokens)
    return tokens


def get_data_from_db(db_name):
    """Select all the text from the database"""
    connect = sqlite3.connect(DB_PATH)
    print("Connecting to database")
    query = connect.cursor()
    query.execute("""SELECT text FROM data""")
    tweets = query.fetchall()
    print("Tweets from databases: %d tweets" % (len(tweets)))
    return tweets


def preprocessing(outfile, label=False):
    """Open the source file and perform the preprocessing
        Added vader labelling as label=True"""
    data = get_data_from_db(DB_PATH)
    # preprocess
    stop_words = set(stopwords.words('english'))
    tweet_list = [preprocess(str(line), stop_words)
                  for line in data]
    if label:
        sid = SentimentIntensityAnalyzer()
        analyzed_data = []
        for text in tweet_list:
            scores = sid.polarity_scores(text)
            analyzed_data.append((text, getlabel(scores), scores['compound']))
        with open(outfile, mode='w', encoding='utf8') as output:
            for tweet in analyzed_data:
                output.write("{},{},{}".format(tweet[0], tweet[1], tweet[2]))
                output.write('\n')
    else:
        with open(outfile, mode='w', encoding='utf8') as output:
            for tweet in tweet_list:
                output.write(tweet)
                output.write('\n')
    print("%d tweets written to file!" % (len(tweet_list)))

if __name__ == "__main__":
    preprocessing(DATA_PATH, True)
