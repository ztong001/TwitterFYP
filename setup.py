# -*- coding: utf-8 -*-
import os

# This is the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
DATA_PATH = os.path.join(ROOT_DIR, r'outData\preprocessed.csv')
DB_PATH = os.path.join(ROOT_DIR, r'db\outdata.db')
print(DATA_PATH)
