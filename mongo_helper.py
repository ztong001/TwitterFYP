# Helper function for MongoDB integration

from pymongo import MongoClient
import json
import logging

client= MongoClient()
db= client['database']
collection= db['sourced']

with open('.\\output291016.txt', 'r') as file_insert:
    for line in file_insert:
        # Some problem here, maybe need regex to define a single line and delimit by /n
        data= json.loads(line)
    logging.debug("Loading data success")

collection.insert_many(data)
logging.debug("Successful insertion")
print(collection.count())
