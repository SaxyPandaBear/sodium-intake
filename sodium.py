import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

import sqlite3

db = sqlite3.connect('sodium.sqlite')
db.row_factory = sqlite3.Row
