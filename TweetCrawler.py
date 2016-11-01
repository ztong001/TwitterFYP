#!/usr/bin/env python

# Copyright 2007-2016 The Python-Twitter Developers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ----------------------------------------------------------------------


import datetime
import json
import logging
import os
import sys
from configobj import ConfigObj
from twitter import Api

# Log for debugging purposes
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:

config= ConfigObj(os.path.abspath('.\\config.ini'))
OAuth= config['AUTH_KEYS']
logging.debug("Loading credentials")
# with open(os.path.abspath('.\\AuthConfig.json')) as authfile:
#     OAuth = json.load(authfile)
#     logging.debug('Loading credentials...')

# Since we're going to be using a streaming endpoint, there is no need to worry
# about rate limits.
twitterapi = Api(OAuth['CONSUMER_KEY'],
                 OAuth['CONSUMER_SECRET'],
                 OAuth['ACCESS_TOKEN'],
                 OAuth['ACCESS_TOKEN_SECRET'],)


def FilterTweet(source):
    """ This helper function filters out the specific fields needed within the
        Twitter stream and returns a json object from the filtered structure
    """
    default= None
    fields_required= config['TWEET']['FORMAT']
    #logging.debug(fields_required)
    filtered_tweet= {field: source[field] if field in source else default for field in fields_required}
    return json.dumps(filtered_tweet,sort_keys=True)

def main():
    number = 0
    filename= "output{:%d%m%y}.txt".format(datetime.date.today())
    logging.debug("Opening twitter stream")
    with open(filename, 'a') as output:
        try:
            for line in twitterapi.GetStreamSample(stall_warnings=True):
                #logging.debug(type(line))
                output.write(FilterTweet(line))
                output.write('\n')
                number += 1
                logging.debug("%s tweets processed" % number)
                #if number == 100:
                    #logging.debug("%s tweets are in!" % number)
                    #break
        except:
            error = str(sys.exc_info())
            logging.exception("Error: %s"%(error))
        finally:
            output.close()
            logging.debug("Closing twitter stream")


if __name__ == '__main__':
    main()
