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

import datetime
import json
import os
import sys
import configparser
from logbook import Logger, StreamHandler
from DBHelper import DBHandler
from twitter.stream import TwitterStream, Timeout, Hangup, HeartbeatTimeout
from twitter.oauth import OAuth

# Logging for debugging purposes
# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
StreamHandler(sys.stdout,encoding='UTF-8').push_application()
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
    """
    default = None
    fields_needed = [field.strip() for field in config['TWEET']['FORMAT'].split(',')]
    # logging.debug(fields_needed)
    filtered_tweet = {field: source[field] if field in source else default for field in fields_needed}
    return filtered_tweet


def stream_tweets():
    """ This is the main streaming function of the TweetCrawler, which collects real-time tweets
        and write them into output text files.
    """
    number = en_tweets = 0
    filename = str(os.getcwd()) + "/outData/output{:%d%m%y}.txt".format(datetime.date.today())
    # Using default Public Stream for now
    stream = TwitterStream(auth=auth, domain="stream.twitter.com", secure=True)
    log.debug("Opening twitter stream")
    with open(filename, 'a') as output:
        for line in stream.statuses.sample():
            if line is Timeout:
                log.warn("Timeout")
            elif line is Hangup:
                log.warn("Hangup")
            elif line is HeartbeatTimeout:
                log.warn("HeartbeatTimeout")
            else:
                tweet = filter_tweet(line)
                #log.debug(tweet)
                if tweet.get('lang') == 'en':
                    en_tweets += 1
                    output.write(json.dumps(tweet, sort_keys=True))
                    output.write("\n")
                    #db.insert_into_collection('source', tweet)
                number += 1
                log.debug("%s english tweets out of %s total processed" % (en_tweets, number))
        log.debug("Closing twitter stream")


def main():
    switch = True
    errlogname = str(os.getcwd()) + "/ErrorLog.txt"
    log.debug("Starting Program")
    #db.start_mongo_database(db_name='test', db_path=r'.\db')
    while (switch):
        try:
            log.debug("Starting the stream")
            stream_tweets()
        except(KeyboardInterrupt):
            log.error("Forced Stop")
            switch = False
        except:
            error = '\n'.join([str(v) for v in sys.exc_info()])
            log.error(error)
            with open(errlogname, 'a') as errlog:
                errlog.write(error)
                errlog.write("\n")
            continue
    log.debug("End of Program")


if __name__ == '__main__':
    main()
