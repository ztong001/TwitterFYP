#!/usr/bin/env python

# Copyright (c) 2008 Mike Verdone

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# ----------------------------------------------------------------------

import time
import json
import os
import sys
import re
from socket import error as SocketError
from collections import defaultdict
from logbook import Logger, StreamHandler, FileHandler
from twitter import Twitter, TwitterHTTPError, TwitterError
from twitter.stream import TwitterStream
from twitter.oauth import OAuth
from TweetModel import TweetModel

# Logging for debugging purposes, errors are logged in an separate file
StreamHandler(sys.stdout, encoding='utf-8').push_application()
FileHandler(filename=(str(os.getcwd()) + "/ErrorLog.txt"), encoding='utf-8',
            level='ERROR').push_application()
# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:
config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as jsonfile:
    config = json.load(jsonfile)
credentials = config['auth_keys']

log = Logger("Twitter Logger")
log.debug("Loading credentials")

# Data output filename here
filename = str(os.getcwd()) + config['tweet']['testjsonl']

# OAuth authentication details here
authKeys = OAuth(consumer_key=credentials['CONSUMER_KEY'],
                 consumer_secret=credentials['CONSUMER_SECRET'],
                 token=credentials['ACCESS_TOKEN'],
                 token_secret=credentials['ACCESS_TOKEN_SECRET'])

# Regex used to filter out retweets
retweets_check = re.compile(r'^RT\s')


def crawl_method(crawlType):
    if crawlType == 'rest':
        return crawl_tweets()
    elif crawlType == 'stream':
        return stream_tweets()
    else:
        print("Invalid crawling type")


# def filter_tweet(source):
#     """ This function filters out the specific fields needed within the
#         Twitter stream and returns a json object from the filtered structure
#     """
#     fields = [('created_at', source['created_at']), ('id', source['id']),
#               ('text', source['text']), ('user', source['user']['name'])]
#     filtered_tweet = defaultdict(None, fields)
#     return filtered_tweet


def crawling(stream):
    """ Creates an array of tweet data in json form from the stream
    """
    tweets = []

    for line in stream:
        if 'text' in line:
            if re.search(retweets_check, line['text']) is None:
                uid = line['id']
                text = line['text']
                user = line['user']['name']
                created_at = line['created_at']
                tweet = TweetModel(uid, text, user, created_at)
                tweets.append(tweet)
                log.debug("%s tweets processed" % (len(tweets)))
        else:
            log.debug("%r" % (line))
    return tweets


def crawl_tweets():
    """ REST API implementation of crawling existing tweets and saving them into a file.
        Not working so far
    """

    log.debug("Activating Twitter REST API")
    stream = Twitter(auth=authKeys, domain="search.twitter.com",
                     api_version="1.1", secure=True)
    stream_iter = stream.search.tweets(
        q=config['tweet']['keywords'], lang='en')
    return stream_iter


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


def main():
    """The core function for the entire workflow
    """
    switch = True
    log.debug("Starting Program")
    while switch:
        try:
            stream = crawl_method(config['tweet']['type'])
            tweets = crawling(stream)
            with open(filename, mode='a', newline='\r\n') as output:
                output.write(json.dumps(tweets))
        except (KeyboardInterrupt, SystemExit):
            log.error("Forced Stop")
            switch = False
            break
        except (TwitterHTTPError, TwitterError, SocketError) as error:
            log.error("Caught Error %s" % str(error))
            log.warn("Sleep for 2 seconds")
            time.sleep(2)
            continue
        finally:
            with open(filename, mode='a', newline='\r\n') as output:
                output.write(json.dumps(tweets))
    log.debug("End of Program")


if __name__ == '__main__':
    main()
