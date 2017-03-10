"""Miscellanous scripts for data migrations across formats"""
import sqlite3
import os
import csv
import json
import setup


def import_file_to_db(input_file):
    """Json/CSV/Txt files to DB"""
    ext = os.path.splitext(input_file)[-1].lower()
    with open(input_file, 'r', newline='\r\n', encoding='utf8') as contents:
        if ext == '.json':
            data = [json.loads(item.strip())
                    for item in contents.read().strip().split('\r\n')]
        elif ext == '.csv':
            data = [item.strip() for item in csv.reader(contents)]
        elif ext == '.txt':
            data = [item.strip()
                    for item in contents.read().strip().split('\r\n')]
    connect = sqlite3.connect(setup.DB_PATH)
    query = connect.cursor()
    for tweet in data:
        query.execute("""INSERT INTO data(id,user,text,created_at) VALUES(?,?,?,?)""",
                      (int(tweet.get('id')), tweet.get('user'), tweet.get('text'), tweet.get('created_at')))
    connect.commit()

if __name__ == '__main__':
    import_file_to_db(setup.DATA_PATH)
