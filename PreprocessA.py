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
emoji_re = re.compile(u'[\U00001000-\U0001FFFF]')
http_re = re.compile(r'^http\S+')


def emoji_translate(char):
    if char in emoji_map:
        caught = emoji_map.get(char)
        print(caught)
        return caught
    else:
        print("not caught")
        return ""


def preprocess_tweets(data):
    # Split sentence into words
    print(type(data))
    tokenized = []
    counter = 0
    for sentence in data:
        print(type(sentence))
        if re.search(emoji_re, sentence) is not None:
            char = re.search(emoji_re, sentence).group()
            sentence = sentence.replace(char, emoji_translate(char))
            counter += 1
            print(counter)
        try:
            sentence = sentence.encode('ascii', 'ignore')
            # Remove links
            sentence = [re.sub(r'^http\S+', '', word) for word in sentence]
            sentence = ' '.join(sentence)
            tokens = tokenizer.tokenize(sentence)
            tokenized.append(tokens)
        except UnicodeEncodeError as e:
            print("Tweet throws %s" % (str(e)))
            continue
    return tokenized


def preprocessing(file):
    """Open the source file and perform the preprocessing"""
    with open(file, 'r', newline='\r\n') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]
    data = [line.get('text') for line in data]

    # preprocess
    stop_words = stopwords.words('english')
    tweet_list = preprocess_tweets(data)

    for tweet in tweet_list:
        print(repr(tweet))

    # with open(csv_name, 'w') as csv_file:
    #     mywriter = csv.writer(csv_file, delimiter='\t')
    #     mywriter.writerows(tweet_list)

if __name__ == "__main__":
    preprocessing(filename)
