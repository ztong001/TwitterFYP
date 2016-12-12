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
import configparser
from logbook import Logger, StreamHandler, FileHandler
from twitter import Twitter, TwitterError, TwitterHTTPError
from twitter.stream import TwitterStream, Timeout, Hangup, HeartbeatTimeout
from twitter.oauth import OAuth

# Logging for debugging purposes, errors are logged in an separate file
# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
errlogname = str(os.getcwd()) + "/ErrorLog.txt"
StreamHandler(sys.stdout,encoding='utf-8').push_application()
FileHandler(filename= errlogname, encoding='utf-8', level='ERROR').push_application()
# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:
config = configparser.ConfigParser(empty_lines_in_values=False)
config.read_file(open(os.path.abspath(r'.\config.ini')))
credentials = config['AUTH_KEYS']

log = Logger("Twitter Logger")
log.debug("Loading credentials")

# Since we're going to be using a streaming endpoint, there is no need to worry
# about rate limits.
auth = OAuth(consumer_key=credentials['CONSUMER_KEY'],
             consumer_secret=credentials['CONSUMER_SECRET'],
             token=credentials['ACCESS_TOKEN'],
             token_secret=credentials['ACCESS_TOKEN_SECRET'])

# Initialise Database Connector
# db = DBHandler()

def filter_tweet(source):
    """ This function filters out the specific fields needed within the
        Twitter stream and returns a json object from the filtered structure
        User name is added in by default.
    """
    default = None
    fields_needed = [field.strip() for field in config['TWEET']['FORMAT'].split(',')]
    # logging.debug(fields_needed)
    filtered_tweet = {field: source[field] if field in source else default for field in fields_needed}
    filtered_tweet.update(user=source['user']['name'])
    return filtered_tweet

def crawl_tweets():
    """ REST API implementation of crawling existing tweets and saving them into a json file.
    """
    number = 0
    filename = str(os.getcwd()) +"/outData/tweetdata.json"
    stream = Twitter(auth=auth, domain="api.twitter.com", secure=True)
    stream_iter = stream.search.tweets(q=config['TWEET']['KEYWORDS'], lang='en')
    log.debug("Activating REST API")
    # Write to a file (Planning to shift this code out to another function)
    with open(filename, 'a') as output:
        for line in stream_iter:
            if line is Timeout:
                log.warn("Timeout")
            elif line is Hangup:
                log.warn("Hangup")
            elif line is HeartbeatTimeout:
                log.warn("HeartbeatTimeout")
            else:
                tweet = filter_tweet(line)
                output.write(tweet)
                number += 1
                log.debug("%s tweets processed" % (number))
        log.debug("Closing twitter stream")

def stream_tweets():
    """ Stream API implementation of crawling real-time tweets and saving them into a json file.
    """
    number = 0
    # filename = str(os.getcwd()) + "/outData/output{:%d%m%y}.txt".format(datetime.date.today())
    filename = str(os.getcwd()) + "/outData/tweetdata.json"

    # Using default Public Stream and stopwords for filter keywords, english tweets only
    stream = TwitterStream(auth=auth, domain="stream.twitter.com", secure=True)
    stream_iter = stream.statuses.filter(track=config['TWEET']['KEYWORDS'], language='en')
    log.debug("Opening twitter stream")
    # Write to a file (Planning to shift this code out to another function)
    with open(filename, 'a') as output:
        for line in stream_iter:
            if line is Timeout:
                log.warn("Timeout")
            elif line is Hangup:
                log.warn("Hangup")
            elif line is HeartbeatTimeout:
                log.warn("HeartbeatTimeout")
            else:
                tweet = filter_tweet(line)
                output.write(tweet)
                number += 1
                log.debug("%s tweets processed" % (number))
        log.debug("Closing twitter stream")


def main():
    """The core function for the entire workflow
    """
    switch = True
    log.debug("Starting Program")
    #db.start_mongo_database(db_name='test', db_path=r'.\db')
    while switch:
        try:
            stream_tweets()
        except KeyboardInterrupt:
            log.warn("Forced Stop")
            switch = False
            break
        except (TwitterError, TwitterHTTPError):
            error = '\n'.join([str(v) for v in sys.exc_info()])
            log.error(error)
            log.warn("Sleep for 90 seconds due to rate limits")
            time.sleep(90)
            continue
    log.debug("End of Program")


if __name__ == '__main__':
    main()
