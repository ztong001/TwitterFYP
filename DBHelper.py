# Helper function for MongoDB integration

import os
import json
import subprocess
# import re
from pymongo import MongoClient

class DBHandler(object):
    """Helper class to manage all database-related operations"""

    def __init__(self):
        self.client = MongoClient(host='localhost', port=27017)

    def start_mongo_database(self, db_name, db_path):
        """Establish a database server"""
        mongod = subprocess.Popen(['mongod', '--dbpath', os.path.abspath(db_path)])
        database = self.client[db_name]
        return "MongoDB set up with {} database on".format(db_name)

    def insert_into_collection(self, collection, data):
        """ Insert one entry into a collection"""
        collection = self.client.database[collection]
        collection.insertOne(data)

    def import_to_database(self, collection, filename):
        """Import files into database NOT TESTED"""
        number = 0
        with open(filename, 'r') as file_insert:
            for line in file_insert:
                # Some problem here, maybe need regex to define a single line and delimit by /n
                collection.insert(line)
                number += 1
                print("%s tweets saved" %number)
            print("Loading data success")

    def stop_mongo_database(self):
        """Stop database connection"""
        self.client.close()
        return "Mongo database closed"

