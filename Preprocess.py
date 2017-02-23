"""preprocessing procedure with POS tagging and tokenisation"""
import os
import sys
import json
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
outfile = str(os.getcwd()) + "/outData/preprocessed.txt"
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
    cleaned_string = p.clean(sentence)
    replaced_string = replacer.replaceAll(cleaned_string)
    tokens = tokenizer.tokenize(replaced_string)
    preprocessed_string = []
    for token, tag in pos_tag(tokens):
        # If stopword, ignore token and continue
        # if token in stop_words:
        #     continue
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
    with open(outfile, 'w') as output:
        for tweet in tweet_list:
            output.write(tweet)
            output.write('\r\n')
    print("%d tweets written to file!" % (len(tweet_list)))

if __name__ == "__main__":
    preprocessing(filename)
