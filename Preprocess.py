"""preprocessing procedure with POS tagging and tokenisation"""
import os
import sys
import json
import csv
import string
import preprocessor as p
import re
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from replacer import ComboReplacer

config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as f:
    config = json.load(f)

lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer(
    strip_handles=True, preserve_case=False, reduce_len=True)
filename = str(os.getcwd()) + config['tweet']['test']
csv_name = str(os.getcwd()) + config['test_csv']
replacer = ComboReplacer()

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
    """Function to tokenise and preprocess a tweet with tweet-preprocessor"""
    tokens = p.clean(sentence.lower())
    tokens = replacer.replaceAll(tokens)
    tokens = tokenizer.tokenize(tokens)
    for token, tag in pos_tag(tokens):
        # If stopword, ignore token and continue
        if token in stop_words:
            continue
        # If punctuation, ignore token and continue
        if all(char in string.punctuation for char in token):
            continue
        # Lemmatize the token and yield
        lemma = lemmatize(token, tag)
        yield lemma
    # tokens = [s.translate(str.maketrans('', '', string.punctuation))
    #           for s in tokens]
    # return tokens


def preprocessing(file):
    """Open the source file and perform the preprocessing"""
    with open(file, 'r', newline='\r\n', encoding='utf8') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]
    print("Number of tweets: {}".format(len(data)))

    # preprocess
    stop_words = set(stopwords.words('english'))
    tweet_list = [preprocess(line.get('text'), stop_words)
                  for line in data]
    # Filter empty strings
    for tweet in tweet_list:
        tweet = " ".join(tweet)
        tweet = tweet.encode('ascii', 'ignore')
        print(tweet)

    # with open(csv_name, 'w') as csv_file:
    #     mywriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    #     mywriter.writerows(tweet_list)

if __name__ == "__main__":
    preprocessing(filename)
