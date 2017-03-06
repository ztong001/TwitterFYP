# -*- coding: utf-8 -*-
import sqlite3
import json
import setup


def import_json():
    with open(setup.DATA_PATH, 'r', newline='\r\n', encoding='utf8') as contents:
        data = [json.loads(item.strip())
                for item in contents.read().strip().split('\r\n')]

    connect = sqlite3.connect(setup.DB_PATH)
    query = connect.cursor()
    for tweet in data:
        query.execute("""INSERT INTO data(id,user,text,created_at) VALUES(?,?,?,?)""",
                      (int(tweet.get('id')), tweet.get('user'), tweet.get('text'), tweet.get('created_at')))
    connect.commit()

if __name__ == '__main__':
    import_json()
