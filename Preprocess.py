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
filename = str(os.getcwd()) + config['tweet']['test']
filename1 = str(os.getcwd()) + "/outdata/tweetdata1.txt"
# connect = sqlite3.connect(db_name)
# query = connect.cursor()
contents = open(filename, 'r', newline='\r\n').read()
data = [item for item in contents.strip().split('\r\n')]
print(type(data))
for line in data:
    print("^" + line + "$")
    tweet = json.loads(line)
    text = tweet.get('text')
    try:
        print(repr(tokenizer.tokenize(text)))
        # query.execute("""INSERT INTO data(id,user,text,created_at)
        # VALUES(?,?,?,?)""",
        # (int(tweet.get('id')), tweet.get('user'), tweet.get('text'), tweet.get('created_at')))
        # connect.commit()
        pass
    except UnicodeEncodeError:
        continue
    except json.decoder.JSONDecodeError as error:
        print(str(error))
    finally:
        print("Done")
        print(len(data))
    # connect.close()
