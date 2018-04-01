#! /usr/bin/env python
from __future__ import print_function
import os
import sys
import re
import tweepy
import random
import requests
USERNAME = 'USER'      #user who will get reply
BOTNAME  = 'prdpXbot'  #our bot_name
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def hacker_news():
    tweet = None
    while tweet is None:
        try:
            post_id = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json").json()[random.randint(1,500)]
            post = requests.get("https://hacker-news.firebaseio.com/v0/item/%d.json"%post_id).json()
            tweet = post["title"] + " "+ post["url"]
        except Exception as shit:
            print(shit)
            tweet = None
    return tweet

def main():
    tweet = hacker_news()
    print(tweet)
    if tweet:
        api.update_status(tweet)

if __name__ == '__main__':
    main()
