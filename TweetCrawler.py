#!/usr/bin/env python

# Copyright (c) 2008 Mike Verdone

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# ----------------------------------------------------------------------

import datetime
import json
import logging
import os
import sys
import configparser
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth
from twitter.util import printNicely

# Log for debugging purposes
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:
config= configparser.ConfigParser(empty_lines_in_values=False)
config.read_file(open(os.path.abspath(r'.\config.ini')))

Cred= config['AUTH_KEYS']
logging.debug("Loading credentials")

# Since we're going to be using a streaming endpoint, there is no need to worry
# about rate limits.
auth = OAuth(consumer_key= Cred['CONSUMER_KEY'],
             consumer_secret= Cred['CONSUMER_SECRET'],
             token= Cred['ACCESS_TOKEN'],
             token_secret= Cred['ACCESS_TOKEN_SECRET'],)

def FilterTweet(source):
    """ This helper function filters out the specific fields needed within the
        Twitter stream and returns a json object from the filtered structure
    """
    default= None
    fields_required= [field.strip() for field in config['TWEET']['FORMAT'].split(',')]
    logging.debug(fields_required)
    filtered_tweet= {field: source[field] if field in source else default for field in fields_required}
    return json.dumps(filtered_tweet,sort_keys=True)

def StreamTweets():
    number=0
    filename= "output{:%d%m%y}.txt".format(datetime.date.today())
	twitterStream = TwitterStream(auth, domain='stream.twitter.com')
    logging.debug("Opening twitter stream")
    with open(filename, 'a') as output:
        for line in twitterStream.statuses.sample():
            output.write(FilterTweet(line)+'\n')
            number += 1
            logging.debug("%s tweets processed" % number)
            #if number == 100:
                #logging.debug("%s tweets are in!" % number)
                #break
        logging.debug("Closing twitter stream")

def main():
    logging.debug("Starting Program")
    ## Endless loop to work around sudden disconnection 
    while True:
        try:
            StreamTweets()
        except (KeyboardInterrupt,SystemExit):
            logging.error("Forced Stop")
            break
        except:
            error = sys.exc_info()[0]
            logging.error("Error: %s"%(error))
            continue
    logging.debug("End of Program")


if __name__ == '__main__':
    main()
