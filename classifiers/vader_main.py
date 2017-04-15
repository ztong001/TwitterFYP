from nltk.sentiment.vader import SentimentIntensityAnalyzer
from evaluation import *
from extensions import label_sentiment


def array_transform(d_list):
    label_binarise = {'pos': 1, 'neg': 2, 'neu': 0}
    transformed = [list(x) for x in zip(*d_list)]
    binarised = [label_binarise[i] for i in transformed[1]]
    return binarised


def vader_run(data):
    sid = SentimentIntensityAnalyzer()
    result = []
    for text in data:
        scores = sid.polarity_scores(text[0])
        line = (text, label_sentiment(scores))
        result.append(line)
    print("{} tweets analysed in vader!".format(len(data)))
    result_binary, target_binary = array_transform(
        result), array_transform(data)

    generate_report(result_binary, 'vader', target_binary)

if __name__ == "__main__":
    dataset = get_dataset('preprocessed.csv')
    vader_run(dataset)
