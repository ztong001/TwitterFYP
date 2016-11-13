# Helper function for MongoDB integration

from pymongo import MongoClient
import json
import logging

client= MongoClient()
db= client['database']
collection= db['sourced']
number=0
with open('.\\output291016.txt', 'r') as file_insert:
    for line in file_insert:
        # Some problem here, maybe need regex to define a single line and delimit by /n
        collection.insert(line)
        number+=1
        logging.debug("%s tweets saved" % number)
    logging.debug("Loading data success")

print(collection.count())
