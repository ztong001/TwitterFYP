This is my senior year project involving opinion mining and sentimental analysis as part of the academic requirement for my Bachelor of Engineering(Computer Science) degree.
Features to be highlighted include a dynamic sentiment lexicon that evolves according to input data and efficent handling of the large amount of user data from the internet.

Project Description:

Most studies on sentiment analysis were conducted in a closed domain setting, where the training and test data are assumed to share a similar vocabulary. However, this assumption does not hold in the context of social media, where the vocabulary is evolutional. In other words, there are always new words/phrases appearing in a social media over time. As a result, the sentiment lexicon built offline from the training data may be out of date when being used to make predictions. The objective of this project is to develop an open-domain sentiment analysis framework to address dynamic issue of vocabulary in social media. The proposed framework should be able to expand a sentiment lexicon for a social media dynamically and automatically. Moreover, the proposed framework should be computationally efficient to handle large-scale social posts generated daily by users in the social media.

Process Flow:

Crawling Tweets -> Preprocessing(Tokenisation/POS-tagging) -> Train model on data -> Build Classifier -> Test on Data

Requirements:
- Python 3.5 and above. I recommend you to download Anaconda [here](https://www.continuum.io/downloads)
- pip install requirements.txt

TODO:
- Sentiment Analysis component (Ensemble classification methods, Training models)
- Develop dynamic sentiment lexicon by referencing custom corpora construction.
- Graphical front-end to show the results of the classification(pywebview, chartjs, bootstrap) *if possible

Credits:
- https://mike.verdone.ca/twitter/ - Python Twitter Tools (by Mike Verdone)
- https://pypi.python.org/pypi/Logbook - LogBook, Python logging library
- https://www.nltk.org - Natural Language Toolkit
- https://github.com/cjhutto/vaderSentiment - VADER Sentiment Analysis tool (within NLTK)
- https://scikit-learn.org/stable - Scikit-Learn library for Machine Learning Algorithms