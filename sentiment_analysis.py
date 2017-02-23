import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

file_in = twitter_samples.strings('tweets.20150430-223406.json')
test_file = str(os.getcwd()) + "\outData\preprocessed.txt"


def vader_analyse(file_input):
    with open(file_input, newline='\r\n') as inputfile:
        sentences = inputfile.readlines()
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        line = line.strip('\r\n')
        print(line.encode('ascii', 'ignore'))
        scores = sid.polarity_scores(line)
        for k in sorted(scores):
            print("{0}:{1}, ".format(k, scores[k]), end='')
        print('\n')

if __name__ == '__main__':
    vader_analyse(test_file)
