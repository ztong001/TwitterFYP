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

import preprocessor as p
from replacer import ComboReplacer
from setup import *

with open(CONFIG_PATH) as f:
    config = json.load(f)

lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer(
    strip_handles=True, preserve_case=False, reduce_len=True)
outfile = os.path.join(ROOT_DIR, "outData/preprocessed.txt")
replacer = ComboReplacer()
# Filter out URLs, mentions, hashtags and emojis
p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG, p.OPT.EMOJI)


def lemmatize(token, tag):
    tag = {
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV,
        'J': wordnet.ADJ
    }.get(tag[0], wordnet.NOUN)

    return lemmatizer.lemmatize(token, tag)


def preprocess(sentence, stop_words):
    """Function to clean, tokenise and preprocess a tweet with tweet-preprocessor"""
    cleaned_string = p.clean(sentence)
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


def preprocessing(dfile):
    """Open the source file and perform the preprocessing"""
    data = get_data_from_db(DB_PATH)
    # preprocess
    stop_words = set(stopwords.words('english'))
    tweet_list = [preprocess(str(line), stop_words)
                  for line in data]
    with open(outfile, mode='w', encoding='utf8') as output:
        for tweet in tweet_list:
            output.write(tweet)
            output.write('\n')
    print("%d tweets written to file!" % (len(tweet_list)))

if __name__ == "__main__":
    preprocessing(DATA_PATH)
