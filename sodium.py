from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import praw
import sqlite3
import multiprocessing
import threading
import datetime
import numpy

import auths

# ================================================================================
# First time setup. Subsequent runs do not require this code block
# import nltk
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# ================================================================================

db = sqlite3.connect('sodium.db')
db.row_factory = sqlite3.Row

# id: the unique post id that reddit gives to each submission
# sentiment: the average compound sentiment from a submission's text
# submission_date: the date and time that the post was submitted
db.execute('CREATE TABLE IF NOT EXISTS sodium (id TEXT PRIMARY KEY, sentiment FLOAT, submission_date TIMESTAMP)')

analyzer = SentimentIntensityAnalyzer()

reddit = praw.Reddit(client_id=auths.client,
                     client_secret=auths.secret,
                     user_agent='saxypandabear:reddit-sentiment-analyzer:v0.1')


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
    timestamp = datetime.datetime.fromtimestamp(submission.created)
    text = submission.selftext

    sentences = sent_tokenize(text)               # tokenize the text within the post
    sentences += sent_tokenize(submission.title)  # include the title of the post

    # for each sentence, calculate the compound sentiment
    # should not have empty list of sentiments because there should be at least a non-empty title
    sentiments = [get_sentence_sentiment(sentence) for sentence in sentences]

    # return the id, the datetime of submission, and the average compound sentiment
    return submission.id, numpy.average(sentiments), timestamp


# uses the NLTK Vader sentiment analyzer to calculate the compound sentiment of a given sentence
def get_sentence_sentiment(sentence):
    return analyzer.polarity_scores(sentence)['compound']


# define the function that will be run indefinitely in the script
def analyze_sentiments():
    threading.Timer(86400, analyze_sentiments).start()  # run this once every day
    pool = multiprocessing.Pool(processes=5)
    submissions = reddit.subreddit(get_subreddits()).hot(limit=50)  # first 2 pages
    results = pool.map(get_submission_sentiment, submissions)
    pool.close()  # close the processes after they are done being used
    # print(results)

    # after getting results, write to DB
    for values in results:
        # print(values)
        db.execute("INSERT OR IGNORE INTO sodium VALUES (?,?,?)", values)
    db.commit()  # after writing all of the items into the database, commit to the disk file


if __name__ == '__main__':
    try:
        while True:
            analyze_sentiments()
    except:
        db.close()  # try to gracefully close the database on KeyboardInterrupt
        exit(0)
