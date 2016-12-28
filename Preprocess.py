"""Preprocessing procedure"""
import json
import os
from nltk.tokenize import TweetTokenizer

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
filename = str(os.getcwd()) + "/outData/tweetdata.txt"
with open(filename, 'r', newline='\r\n') as f:
    for line in f:
        tweet = json.loads(line)
        text = tweet.get('text')
        try:
            print(repr(tokenizer.tokenize(text)))
        except UnicodeEncodeError:
            continue
