from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from features import label_feats_from_corpus, split_label_feats
# >>> from nltk.corpus import movie_reviews
# >>> from featx import label_feats_from_corpus, split_label_feats
# >>> movie_reviews.categories()
# ['neg', 'pos']
# >>> lfeats = label_feats_from_corpus(movie_reviews)
# >>> lfeats.keys()
# dict_keys(['neg', 'pos'])
# >>> train_feats, test_feats = split_label_feats(lfeats)
# >>> len(train_feats)
# 1500
# >>> len(test_feats)
# 500

mnb_classifier = SklearnClassifier(MultinomialNB())
mnb_classifier.train(train_features)
mnb_accuracy = accuracy(sk_classifier, test_features)
svc_classifier = SklearnClassifier(LinearSVC()).train(train_feats)
