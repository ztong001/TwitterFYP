"""Main evaluation function"""

import multi_nb
import word2vec
import vader_main
from evaluation import get_dataset

if __name__ == '__main__':
    dataset = get_dataset('preprocessed.csv')
    vader_main.vader_run(dataset)
    word2vec.word2vec_classifier(dataset)
    multi_nb.mnb_classifier(dataset)
