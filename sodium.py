# NLP imports
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

# Reddit imports
import praw

# Database imports
import sqlite3

db = sqlite3.connect('sodium.db')
db.row_factory = sqlite3.Row
