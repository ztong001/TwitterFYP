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
import logging
import os
import sys
import configparser
from DBHelper import DBHandler
from twitter.stream import TwitterStream, Timeout, Hangup, HeartbeatTimeout
from twitter.oauth import OAuth

# Log for debugging purposes
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:
config = configparser.ConfigParser(empty_lines_in_values=False)
config.read_file(open(os.path.abspath(r'.\config.ini')))
Cred = config['AUTH_KEYS']
logging.debug("Loading credentials")

# Since we're going to be using a streaming endpoint, there is no need to worry
# about rate limits.
auth = OAuth(consumer_key=Cred['CONSUMER_KEY'],
             consumer_secret=Cred['CONSUMER_SECRET'],
             token=Cred['ACCESS_TOKEN'],
             token_secret=Cred['ACCESS_TOKEN_SECRET'])

# Initialise Database Connector
db= DBHandler()

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
    stream = TwitterStream(auth=auth, domain="stream.twitter.com",secure=True)
    logging.debug("Opening twitter stream")
    with open(filename, 'a') as output:
        for line in stream.statuses.sample():
            if line is Timeout:
                logging.debug("Timeout")
            elif line is Hangup:
                logging.debug("Hangup")
            elif line is HeartbeatTimeout:
                logging.debug("HeartbeatTimeout")
            else:
                tweet = filter_tweet(line)
                #logging.debug(tweet)
                if tweet.get('lang') == 'en':
                    en_tweets += 1
                    output.write(json.dumps(tweet, sort_keys=True))
                    output.write("\n")
                    db.insert_into_collection('source', tweet)
                number += 1
                logging.debug("%s english tweets out of %s total processed" % (en_tweets, number))
        logging.debug("Closing twitter stream")


def main():
    logging.debug("Starting Program")
    db.start_mongo_database(db_name='test', db_path=r'.\db')
    # Endless loop to work around sudden disconnection
    while True:
        try:
            stream_tweets()
        except (KeyboardInterrupt, SystemExit):
            logging.error("Forced Stop")
            break
        except:
            error = '\n'.join([str(v) for v in sys.exc_info()])
            logging.exception("Error: %s" % (error))
            # continue
            break
        finally:
            db.stop_mongo_database()
    logging.debug("End of Program")


if __name__ == '__main__':
    main()
