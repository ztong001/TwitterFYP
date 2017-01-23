"""Preprocessing procedure"""
import json
import os
import re
import string
# import sqlite3
import nltk
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
    elif word == "'s" and pos_tag == "VBZ":
        word = "is"
    return word

tokenizer = TweetTokenizer(
    strip_handles=True, reduce_len=True, preserve_case=False)
db_name = str(os.getcwd()) + config['db_name']
filename = str(os.getcwd()) + config['tweet']['testjsonl']
# connect = sqlite3.connect(db_name)
# query = connect.cursor()


def preprocess_tweets(data, stop_words):
    # Split sentence into words
    processed_data = [line.split() for line in data]

    tweet_list = []
    for sentence in processed_data:
        # Remove links
        sentence = [
            word.decode(encoding='utf-8') for word in sentence if not re.search(r"^http\S+", str(word))]
        tweet_text = ' '.join(sentence)
        tweet_list.append(tweet_text)

    # Lemmatization
    for i, tweet in enumerate(tweet_list):
        tweet = tweet_list[i]
        tokens = tokenizer.tokenize(tweet)

        preprocessed_string = []
        for (word, pos_tag) in nltk.pos_tag(tokens):
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
    tweet_list = [re.sub('[%s]' % re.escape(
        string.punctuation), '', sentence) for sentence in tweet_list]

    return tweet_list


def preprocessing(file):
    """Open the source file and perform the preprocessing"""
    with open(file, 'r', newline='\r\n') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]
    data = [line.get('text').encode('utf-8', 'ignore') for line in data]

    # preprocess
    stop_words = stopwords.words('english')
    tweet_list = preprocess_tweets(data, stop_words)

    # TODO: Write to CSV

if __name__ == "__main__":
    preprocessing(filename)
