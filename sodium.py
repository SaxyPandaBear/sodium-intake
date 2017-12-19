from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import praw
import sqlite3
import multiprocessing
import numpy

import auths

# First time setup requires vader_lexicon
# import nltk
# nltk.download('vader_lexicon')

db = sqlite3.connect('sodium.db')
db.row_factory = sqlite3.Row

# id: the unique post id that reddit gives to each submission
# sentiment: the average compound sentiment from a submission's text
db.execute('CREATE TABLE IF NOT EXISTS sodium (id TEXT PRIMARY KEY, sentiment FLOAT)')

analyzer = SentimentIntensityAnalyzer()

reddit = praw.Reddit(client_id=auths.client,
                     client_secret=auths.secret,
                     user_agent='saxypandabear:reddit-sentiment-analyzer:v0.1')

pool = multiprocessing.Pool(processes=10)


# takes a list and returns a concatenation of the items.
# [a,b,c] => "a+b+c"
def get_subreddits():
    with open('subreddits.txt', 'r') as file:
        subs = file.read().splitlines()  # readlines() returns strings with newline characters
    return '+'.join(list(filter(None, subs)))


# takes a submission and returns the average compound sentiment for the text,
# as well as the submission id
# positive sentiments are > 0, negative sentiments are < 0, neutral is 0.
def get_submission_sentiment(submission):
    text = submission.selftext
    sentences = sent_tokenize(text)
    sentence_sentiments = pool.map_async(get_sentence_sentiment, sentences)

    return submission.id, numpy.average(sentence_sentiments.get())


def get_sentence_sentiment(sentence):
    return analyzer.polarity_scores(sentence)['compound']


submissions = reddit.subreddit(get_subreddits()).hot(limit=100)
results = pool.map(get_submission_sentiment, submissions)

print(results)
