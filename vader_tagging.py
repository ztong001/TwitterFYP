"""Data Labelling with Vader sentiment"""
import sqlite3

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tablib import Dataset
import preprocessor as pre
from setup import DATA_PATH, DB_PATH

# Filter out URLs, mentions, hashtags and emojis
pre.set_options(pre.OPT.URL, pre.OPT.MENTION,
                pre.OPT.HASHTAG, pre.OPT.EMOJI)


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
    print("Connecting to database")
    query = sqlite3.connect(DB_PATH).cursor()
    query.execute(
        "SELECT text FROM data ORDER BY id DESC LIMIT " + str(number) + "; ")
    tweets = [line[0] for line in query.fetchall()]
    print("Tweets from databases: %d tweets" % (len(tweets)))
    return tweets


def save_data_to_db(labelled):
    """Save labelled data to database"""
    add_query = sqlite3.connect(DB_PATH).cursor()
    add_query.execute(
        "CREATE TABLE IF NOT EXISTS labels(text TEXT, label TEXT, score FLOAT)")
    for entry in labelled:
        add_query.execute("""INSERT INTO labels(text,label,score) VALUES(?,?,?)""",
                          (entry))
    return


def vader_analyse(file_input):
    """Labels the dataset with vader sentiment tool"""
    sentences = getdata_from_db(1000)
    print("Working on %d tweets" % (len(sentences)))
    headers = ('text', 'label', 'score')
    analyzed_data = []
    sid = SentimentIntensityAnalyzer()
    for line in sentences:
        text = pre.clean(line)
        scores = sid.polarity_scores(text)
        analyzed_data.append((text, getlabel(scores), scores['compound']))
    save_data_to_db(analyzed_data)
    analyzed = Dataset(*analyzed_data, headers=headers)
    return analyzed

if __name__ == '__main__':
    analyzed_file = vader_analyse(DATA_PATH)
    with open('analyzed.csv', 'w', encoding='utf8') as csvfile:
        csvfile.write(analyzed_file.csv)
    print("Saved %d tweets" % (len(analyzed_file)))
