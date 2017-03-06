# -*- coding: utf-8 -*-
import os

# This is the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
SA_PATH = os.path.join(ROOT_DIR, r'SADataset.csv')
DATA_PATH = os.path.join(ROOT_DIR, r'outData\preprocessed.txt')
DB_PATH = os.path.join(ROOT_DIR, r'db\outdata.db')
print(DATA_PATH)
