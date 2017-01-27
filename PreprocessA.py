import os
import json
import csv
import re
import nltk
from emoji import emoji_map
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as f:
    config = json.load(f)

tokenizer = TweetTokenizer(strip_handles=True, preserve_case=False)
filename = str(os.getcwd()) + config['tweet']['testjsonl']
csv_name = str(os.getcwd()) + config['test_csv']
emoji_re = re.compile(r'(\\)(U000)(1|0)(\w|\d){4}')


def emoji_translate(char):
    if char in emoji_map:
        return emoji_map.get(char)
    else:
        return ""


def preprocess_tweets(data):
    # Split sentence into words
    processed_data = [line.strip() for line in data]
    tokenized = []
    for sentence in processed_data:
        if re.search(emoji_re, sentence) is not None:
            char = re.search(emoji_re, sentence).group()
            print("caught letter %s" % (char))
            sentence.replace(char, emoji_translate(char))
        try:
            tokens = tokenizer.tokenize(sentence)
            tokenized.append(tokens)
        except UnicodeEncodeError as e:
            print("Tweet throws %s" % (str(e)))
            continue
    return tokenized


def preprocessing(file):
    """Open the source file and perform the preprocessing"""
    with open(file, 'r', encoding='utf-8', newline='\r\n') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]
    data = [line.get('text') for line in data]

    # preprocess
    stop_words = stopwords.words('english')
    tweet_list = preprocess_tweets(data)

    with open(csv_name, 'w') as csv_file:
        mywriter = csv.writer(csv_file, delimiter='\t')
        mywriter.writerows(tweet_list)

if __name__ == "__main__":
    preprocessing(filename)
