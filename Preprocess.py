"""Preprocessing procedure"""
import json
import os
import re
import string
import sys
# import sqlite3
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as f:
    config = json.load(f)

lemmatizer = WordNetLemmatizer()


def wordnet_pos_code(tag):
    if tag is None:
        return ''
    elif tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''


def transform_apostrophe(word, pos_tag):
    if word == "n't":
        word = "not"
    elif word == "'ll":
        word = "will"
    elif word == "'re":
        word = "are"
    elif word == "'ve":
        word = "have"
    elif word == "'s" and posTag == "VBZ":
        word = "is"
    return word

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
db_name = str(os.getcwd()) + config['db_name']
filename = str(os.getcwd()) + config['tweet']['testjsonl']
# connect = sqlite3.connect(db_name)
# query = connect.cursor()
with open(filename, 'r', newline='\r\n') as contents:
    data = [json.loads(item.strip())
            for item in contents.read().strip().split('\r\n')]
data = [line.get('text') for line in data]


def preprocess_tweets(data, stop_words):
    # Split sentence into lowercase words
    processed_data = [line.lower().split() for line in data]

    tweet_list = []
    for sentence in processed_data:
        # Remove links
        sentence = [
            word for word in sentence if not re.match(r"^http\S+", word)]
        tweet_text = " ".join(sentence)
        tweet_list.append(tweet_text)

    # Lemmatization
    for i in range(len(tweet_list)):
        tweet = tweet_list[i]
        tokens = tokenizer.tokenize(tweet)

        preprocessed_string = []
        for (word, pos_tag) in pos_tag(tokens):
            word = transform_apostrophe(word, pos_tag)
            # Skip if it is stopwords
            if word in stop_words:
                continue
            elif pos_tag != None and pos_tag in [".", "TO", "IN", "DT", "UH", "WDT", "WP", "WP$", "WRB"]:
                continue

            if wordnet_pos_code(pos_tag) != "":
                word = lemmatizer.lemmatize(word, wordnet_pos_code(pos_tag))
            preprocessed_string.append(word)

        tweet_list[i] = " ".join(preprocessed_string)

    # Remove punctuation
    for i in range(len(tweet_list)):
        sentence = tweet_list[i]
        sentence = sentence.encode('utf-8').translate(None, string.punctuation)
        tweet_list[i] = sentence

    return tweet_list

if __name__ == "__main__":
    preprocess_tweets(data, stopwords)
