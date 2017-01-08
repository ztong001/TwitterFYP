"""Preprocessing procedure"""
import json
import os
import sys
import sqlite3
from nltk.tokenize import TweetTokenizer

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
db_name = str(os.getcwd()) + "/db/outdata.db"
filename = str(os.getcwd()) + "/outData/tweetdata.txt"
filename1 = str(os.getcwd()) + "/outData/tweetdata1.txt"
connect = sqlite3.connect(db_name)
query = connect.cursor()
with open(filename, 'r', newline='\r\n') as f:
    for line in f:
        tweet = json.loads(line)
        text = tweet.get('text')
        try:
            print(repr(tokenizer.tokenize(text)))
            query.execute("""INSERT INTO data(id,user,text,created_at) VALUES(?,?,?,?)""",
                          (int(tweet.get('id')), tweet.get('user'), tweet.get('text'), tweet.get('created_at')))
            connect.commit()
        except UnicodeEncodeError:
            continue
        except json.decoder.JSONDecodeError:
            print(repr(sys.exc_info()[0]))
            last_position = f.tell()
            new_file = open(filename1, 'w')
            new_file.write(f.seek(last_position))
            new_file.close()
        finally:
            print("Done")
    connect.close()
