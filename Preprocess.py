"""Preprocessing procedure"""
import json
import os
import sys
import sqlite3
from nltk.tokenize import TweetTokenizer

config_filename = str(os.getcwd()) + "/config.json"
with open(config_filename) as f:
    config = json.load(f)
tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
db_name = str(os.getcwd()) + config['db_name']
filename = str(os.getcwd()) + config['tweet']['testjsonl']
filename1 = str(os.getcwd()) + "/outdata/tweetdata1.txt"
# connect = sqlite3.connect(db_name)
# query = connect.cursor()
contents = open(filename, 'r').read()
data = [json.loads(str(item)) for item in contents.strip().split('\r\n')]
contents.close()
for line in data:
    print(line)
    text = line.get('text')
    try:
        print(repr(tokenizer.tokenize(text)))
        # query.execute("""INSERT INTO data(id,user,text,created_at)
        # VALUES(?,?,?,?)""",
        # (int(tweet.get('id')), tweet.get('user'), tweet.get('text'), tweet.get('created_at')))
        # connect.commit()
    except UnicodeEncodeError:
        continue
    except json.decoder.JSONDecodeError as error:
        print(str(error))
    finally:
        print("Done")
    # connect.close()
