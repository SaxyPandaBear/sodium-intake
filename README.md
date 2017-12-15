Sodium Intake - A Reddit Sentiment Analyzer
===========================================

Scrapes subreddits for hot posts daily, and performs sentiment analysis 
on the set of submissions to gauge an overall sentiment for posts in the 
selected subreddits.

## Setup and Installation

- Uses [NLTK](http://www.nltk.org/) and [PRAW](https://praw.readthedocs.io/en/latest/)
- You can install all of the required dependencies by running pip on the `requirements.txt` file
    - `pip install -r requirements.txt`
    - Note: These are the only *requirements* to use this application. NLTK itself has other libraries that is uses,
      and will give warnings when those libraries are not installed.
        - To fix this for `twython`, just install it. `pip install twython`
- Create an `auths.py` file. Template is provided.
    - You must register a Reddit application [here](https://www.reddit.com/prefs/apps) in order to
      obtain your client ID and secret for using Reddit's API.
- 

TBD

## Usage

TBD

