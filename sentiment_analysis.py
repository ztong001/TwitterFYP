import os
from setup import DATA_PATH
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

file_in = twitter_samples.strings('tweets.20150430-223406.json')


def vader_analyse(file_input):
    with open(file_input, encoding='utf8') as inputfile:
        sentences = inputfile.readlines()
    print("Working on %d tweets" % (len(sentences)))
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        line = line.strip('\r\n')
        print(line.encode('ascii', 'ignore'))
        scores = sid.polarity_scores(line)
        for k in sorted(scores):
            print("{0}:{1}, ".format(k, scores[k]), end='')
        print('\n')

if __name__ == '__main__':
    vader_analyse(DATA_PATH)
