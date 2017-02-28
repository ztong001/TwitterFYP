import csv
from tablib import Dataset
from setup import DATA_PATH
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

file_in = twitter_samples.strings('tweets.20150430-223406.json')
file_positive = twitter_samples.strings('positive_tweets.json')
file_negative = twitter_samples.strings('negative_tweets.json')


def getlabel(scores):
    """Label the tweet as pos/neg/neu based on the largest value attribute"""
    checked = {'pos': scores['pos'], 'neg': scores[
        'neg'], 'neu': scores['neu']}
    return max(checked, key=lambda key: checked[key])


def vader_analyse(file_input):
    with open(file_input, encoding='utf8') as inputfile:
        sentences = inputfile.readlines()
    print("Working on %d tweets" % (len(sentences)))
    headers = ('text', 'label', 'pos', 'neg', 'neu')
    analyzed_data = []
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        line = line.strip('\r\n')
        # print(line.encode('ascii', 'ignore'))
        scores = sid.polarity_scores(line)
        analyzed_data.append(
            (line, getlabel(scores), scores['pos'], scores['neg'], scores['neu']))
    analyzed = Dataset(*analyzed_data, headers=headers)
    return analyzed
if __name__ == '__main__':
    analyzed_file = vader_analyse(DATA_PATH)
    with open('analyzed.csv', 'w', encoding='utf8') as csvfile:
        csvfile.write(analyzed_file.csv)
    print("Saved %d tweets" % (len(analyzed_file)))
