"""Main evaluation function"""

import multi_nb
import word2vec
import vader_main
from evaluation import get_dataset

if __name__ == '__main__':
    print("Getting dataset")
    dataset = get_dataset('preprocessed.csv')
    print("Running Vader")
    vader_main.vader_run(dataset)
    print("Running w2c with Linear SVC")
    word2vec.word2vec_classifier(dataset)
    print("Running Multinominal Naive Bayes")
    multi_nb.mnb_classifier(dataset)
    print("Done!")
