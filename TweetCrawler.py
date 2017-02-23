# -*- coding: utf-8 -*-

import time
import json
from setup import ROOT_DIR, CONFIG_PATH
import os
import sys
import re
from socket import error as SocketError
from logbook import Logger, StreamHandler, FileHandler
from twitter import TwitterHTTPError, TwitterError
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth

# Logging for debugging purposes, errors are logged in an separate file
StreamHandler(sys.stdout, encoding='utf-8').push_application()
FileHandler(filename=(str(os.getcwd()) + "/ErrorLog.txt"), encoding='utf-8',
            level='ERROR').push_application()
# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:
# config_filename = str(os.getcwd()) + "/config.json"
with open(CONFIG_PATH) as jsonfile:
    config = json.load(jsonfile)
credentials = config['auth_keys']

log = Logger("Twitter Logger")
log.debug("Loading credentials")

# Data output filename here
filename = os.path.join(ROOT_DIR, config['tweet']['file'])

# OAuth authentication details here
authKeys = OAuth(consumer_key=credentials['CONSUMER_KEY'],
                 consumer_secret=credentials['CONSUMER_SECRET'],
                 token=credentials['ACCESS_TOKEN'],
                 token_secret=credentials['ACCESS_TOKEN_SECRET'])

# Regex used to filter out retweets
retweets_check = re.compile(r'^RT\s')


class TweetModel:
    """Data Format for tweet to be analysed
    """

    def __init__(self, uid, text, user, created_at):
        self.uid = uid
        self.text = text
        self.user = user
        self.created_at = created_at

    def to_dict(self):
        """Returns a dictionary representation of the Tweet
        """
        return {
            "id": self.uid, "text": self.text, "user": self.user, "created_at": self.created_at}


def stream_tweets():
    """ Stream API implementation of crawling real-time tweets and saving them into a file.
    """

    # filename = str(os.getcwd()) + "/outData/output{:%d%m%y}.txt".format(datetime.date.today())
    # Using default Public Stream and stopwords for filter keywords, english
    # tweets only
    log.debug("Activating Twitter Stream API")
    stream = TwitterStream(
        auth=authKeys, domain="stream.twitter.com", secure=True)
    stream_iter = stream.statuses.filter(
        track=(config['tweet']['keywords']), language='en')
    return stream_iter


if __name__ == '__main__':
    """The core function for the entire workflow
    """
    switch = True
    log.debug("Starting Program")
    while switch:
        try:
            # stream = crawl_method(config['tweet']['type'])
            stream = stream_tweets()
            tweets = []
            with open(filename, mode='a') as output:
                for line in stream:
                    if 'text' in line:
                        # if re.search(retweets_check, line['text']) is None:
                        tweet = TweetModel(line['id'], line['text'], line[
                            'user']['name'], line['created_at'])
                        tweets.append(tweet)
                        json.dump(tweet.to_dict(), output, sort_keys=True)
                        output.write('\r\n')
                        log.debug("%s tweets processed" % (len(tweets)))
                    # if len(tweets) == 100:
                    #     switch = False
                    #     break
                    elif line is Timeout:
                        log.debug("-- Timeout --")
                    elif line is HeartbeatTimeout:
                        log.debug("-- Heartbeat Timeout --")
                    elif line is Hangup:
                        log.debug("-- Hangup --")
        except (KeyboardInterrupt, SystemExit):
            log.error("Forced Stop")
            switch = False
            break
        except (TwitterHTTPError, TwitterError, SocketError) as error:
            log.error("Caught Error %s" % str(error))
            log.warn("Sleep for 90 seconds")
            time.sleep(90)
            continue
    log.debug("End of Program")
