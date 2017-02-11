"""Preprocessing procedure with POS tagging and tokenisation"""
import os
import sys
import json
import csv
import string
import re
import nltk
from emoji import emoji_map
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as f:
    config = json.load(f)

lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer(
    strip_handles=True, preserve_case=False, reduce_len=True)
filename = str(os.getcwd()) + config['tweet']['test']
csv_name = str(os.getcwd()) + config['test_csv']
emoji_re = re.compile(u'[\U00001000-\U0001FFFF]')
http_re = re.compile(r'http\S+')
apostrophe_re = re.compile(r'^[A-Za-z](\')[A-Za-z]')


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
    if "n't" in word:
        word = word.strip("n't") + " not"
    elif "'m" in word:
        word = word.strip("'m") + " am"
    elif "'ll" in word:
        word = word.strip("'ll") + " will"
    elif "'re" in word:
        word = word.strip("'re") + " are"
    elif "'ve" in word:
        word = word.strip("'ve") + " have"
    elif "'s" in word and pos_tag == "VBZ":
        word = word.strip("'s") + " is"
    return word


def emoji_translate(char):
    """Translate emoji unicode to short-text descriptions"""
    if char in emoji_map:
        caught = emoji_map.get(char)
        print(caught)
        return caught
    else:
        print("not caught")
        return ""


def preprocess_tweet(sentence, stop_words):
    """Function to tokenise and preprocess a single tweet"""
    # if re.search(emoji_re, sentence) is not None:
    #     char = re.search(emoji_re, sentence).group()
    #     sentence = sentence.replace(char, emoji_translate(char))
    try:
        # Remove links
        result = re.sub(http_re, '', sentence)
        result = re.sub(emoji_re, '', result)
        result = result.encode('ascii', 'ignore')
        tokens = tokenizer.tokenize(result)

        # TODO: Optimise POS tagging
        preprocessed_string = []
        for (word, pos_tag) in nltk.pos_tag(tokens):
            word = transform_apostrophe(word, pos_tag)
            # # Skip if it is stopwords
            # if word in stop_words:
            #     continue
            # elif pos_tag != None and pos_tag in [".", "TO", "IN", "DT", "UH", "WDT", "WP", "WP$", "WRB"]:
            #     continue
            if wordnet_pos_code(pos_tag) != "":
                word = lemmatizer.lemmatize(
                    word, wordnet_pos_code(pos_tag))
            preprocessed_string.append(word)
            # tokenized[i] = " ".join(preprocessed_string)

        # Remove punctuation
        tokens = [s.translate(str.maketrans('', '', string.punctuation))
                  for s in preprocessed_string]
    except UnicodeEncodeError as error:
        print("Tweet throws %s" % (str(error)))
    return tokens


def preprocessing(file):
    """Open the source file and perform the preprocessing"""
    with open(file, 'r', newline='\r\n', encoding='utf8') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]
    print("Number of tweets: {}".format(len(data)))

    # preprocess
    stop_words = set(stopwords.words('english'))
    tweet_list = [preprocess_tweet(
        line.get('text'), stop_words) for line in data]
    # Filter empty strings
    for tweet in tweet_list:
        tweet = " ".join(tweet)
        print(tweet)

    with open(csv_name, 'w') as csv_file:
        mywriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        mywriter.writerows(tweet_list)

if __name__ == "__main__":
    preprocessing(filename)
