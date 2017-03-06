import sqlite3
from tablib import Dataset
from setup import DATA_PATH, DB_PATH
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def getlabel(scores):
    """Label the tweet as pos/neg/neu based on the compound attribute"""
    main_score = scores['compound']
    if main_score > 0.1:
        return 'pos'
    elif main_score < -0.1:
        return 'neg'
    else:
        return 'neu'


def getdata_from_db(number):
    """Select set num of text entries from the database"""
    connect = sqlite3.connect(DB_PATH)
    print("Connecting to database")
    query = connect.cursor()
    query.execute(
        "SELECT text FROM data ORDER BY id LIMIT " + str(number) + "; ")
    tweets = [line[0] for line in query.fetchall()]
    print("Tweets from databases: %d tweets" % (len(tweets)))
    return tweets


# def getdata_from_file(file_input):
#     with open(file_input, encoding='utf8') as inputfile:
#         sentences = inputfile.readlines()
#     return sentences


def vader_analyse(file_input):
    """Labels the dataset with vader sentiment tool"""
    sentences = getdata_from_db(1000)
    print("Working on %d tweets" % (len(sentences)))
    headers = ('text', 'label')
    analyzed_data = []
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        # text = line.encode('ascii', 'ignore')
        # print(line.encode('ascii', 'ignore'))
        scores = sid.polarity_scores(line)
        analyzed_data.append((line, getlabel(scores)))
    analyzed = Dataset(*analyzed_data, headers=headers)
    return analyzed

if __name__ == '__main__':
    analyzed_file = vader_analyse(DATA_PATH)
    with open('analyzed.csv', 'w', encoding='utf8') as csvfile:
        csvfile.write(analyzed_file.csv)
    print("Saved %d tweets" % (len(analyzed_file)))
