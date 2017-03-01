import sqlite3
from tablib import Dataset
from setup import DATA_PATH, DB_PATH
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

file_in = twitter_samples.strings('tweets.20150430-223406.json')
file_positive = twitter_samples.strings('positive_tweets.json')
file_negative = twitter_samples.strings('negative_tweets.json')


def getlabel(scores):
    """Label the tweet as pos/neg/neu based on the compound attribute"""
    main_score = round(scores['compound'])
    if main_score == 1:
        return 'pos'
    elif main_score == -1:
        return 'neg'
    else:
        return 'neu'


def getdata_from_db():
    """Select random 100 text entries from the database"""
    connect = sqlite3.connect(DB_PATH)
    print("Connecting to database")
    query = connect.cursor()
    query.execute(
        """SELECT text FROM data ORDER BY id LIMIT 100; """)
    tweets = query.fetchall()
    print("Tweets from databases: %d tweets" % (len(tweets)))
    return tweets


def getdata_from_file(file_input):
    with open(file_input, encoding='utf8') as inputfile:
        sentences = inputfile.readlines()
    return sentences


def vader_analyse(file_input, db=False):
    if db is False:
        sentences = getdata_from_file(file_input)
    else:
        sentences = getdata_from_db()
    print("Working on %d tweets" % (len(sentences)))
    headers = ('text', 'label', 'pos', 'neg', 'neu')
    analyzed_data = []
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        text = line[0]
        # print(line.encode('ascii', 'ignore'))
        scores = sid.polarity_scores(text)
        analyzed_data.append(
            (text, getlabel(scores), scores['pos'], scores['neg'], scores['neu']))
    analyzed = Dataset(*analyzed_data, headers=headers)
    return analyzed

if __name__ == '__main__':
    analyzed_file = vader_analyse(DATA_PATH, True)
    with open('analyzed.csv', 'w', encoding='utf8') as csvfile:
        csvfile.write(analyzed_file.csv)
    print("Saved %d tweets" % (len(analyzed_file)))
