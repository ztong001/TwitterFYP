import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

sentences = twitter_samples.strings('tweets.20150430-223406.json')
test_file = str(os.getcwd()) + "\outData\preprocessed.txt"
with open(test_file, newline='\r\n') as inputfile:
    test_input = inputfile.readlines()
sid = SentimentIntensityAnalyzer()
for line in test_input:
    line = line.strip('\r\n')
    print(line.encode('ascii', 'ignore'))
    scores = sid.polarity_scores(line)
    for k in sorted(scores):
        print("{0}:{1}, ".format(k, scores[k]), end='')
    print()
