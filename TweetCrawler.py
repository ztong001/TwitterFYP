# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import time
import sqlite3
from socket import error as SocketError

from logbook import FileHandler, Logger, StreamHandler

from setup import *
from twitter import Twitter, TwitterError, TwitterHTTPError
from twitter.util import printNicely
from twitter.oauth import OAuth
from twitter.stream import Hangup, HeartbeatTimeout, Timeout, TwitterStream

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

    def to_tuple(self):
        """Returns a tuple representation of the Tweet
        """
        return (self.uid, self.user, self.text, self.created_at)


def user_tweets():
    """ REST API implementation of crawling tweets from a certain user
    """
    log.debug("From news")
    user = config['tweet']['users']
    rest = Twitter(auth=authKeys)
    results = rest.statuses.user_timeline(screen_name=user)
    return results


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
    connect = sqlite3.connect(DB_PATH)
    query = connect.cursor()
    log.debug("Connecting to Database %s" % (str(DB_PATH)))
    while switch:
        try:
            log.debug("Opening stream")
            stream = stream_tweets()
            tweets = []
            for line in stream:
                if 'text' in line:
                    if re.search(retweets_check, line['text']) is None:
                        tweet = TweetModel(line['id'], line['text'], line[
                            'user']['name'], line['created_at'])
                        tweets.append(tweet.to_tuple())
                        query.execute("""INSERT INTO data(id,user,text,created_at) VALUES(?,?,?,?)""",
                                      tweet.to_tuple())
                        log.debug("%s tweets processed" % (len(tweets)))
                # if len(tweets) == 2999:
                #     switch = False
                #     break
                elif line is Timeout:
                    log.debug("-- Timeout --")
                elif line is HeartbeatTimeout:
                    log.debug("-- Heartbeat Timeout --")
                elif line is Hangup:
                    log.debug("-- Hangup --")
                elif 'timestamp' in line:
                    printNicely("Caught: %r" % (line))
        except (KeyboardInterrupt, SystemExit):
            log.error("Forced Stop")
            switch = False
            break
        except (TwitterHTTPError, TwitterError) as error:
            log.error("Caught Error %s" % str(error))
            log.warn("Sleep for 90 seconds")
            time.sleep(90)
            continue
        except (sqlite3.IntegrityError) as db_error:
            log.error("Caught Error %s" % str(db_error))
            time.sleep(5)
            continue
        finally:
            # query.executemany("""INSERT INTO data(id,user,text,created_at) VALUES(?,?,?,?)""",
            #                   tweets)
            log.debug("Storing %s tweets" % (len(tweets)))
            connect.commit()
    log.debug("End of Program")
