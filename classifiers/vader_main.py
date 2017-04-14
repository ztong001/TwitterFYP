from nltk.sentiment.vader import SentimentIntensityAnalyzer
from evaluation import *
from extensions import label_sentiment


def vader_run(data):
    target = zip(data[0], data[2])
    sid = SentimentIntensityAnalyzer()
    result = []
    for text in data:
        scores = sid.polarity_scores(text[0])
        line = (text, label_sentiment(scores['compound']))
        result.append(line)

    generate_report(result, 'vader', target)

if __name__ == "__main__":
    dataset = get_dataset('preprocessed.csv')
    vader_run(dataset)
