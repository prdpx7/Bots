#! /usr/bin/env python
from __future__ import print_function

import os
from datetime import datetime
import sys

import tweepy
import random
import requests

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def get_hn_url():
    curr_hour = datetime.now().hour
    # shuffle api url b/w top stories and new stories
    if curr_hour % 2:
        return "https://hacker-news.firebaseio.com/v0/topstories.json"
    return "https://hacker-news.firebaseio.com/v0/newstories.json"


def hacker_news():
    tweet = None
    while tweet is None:
        try:
            url = get_hn_url()
            story_ids = requests.get(url).json()
            story_id = story_ids[random.randint(0, len(story_ids))]
            story = requests.get(
                "https://hacker-news.firebaseio.com/v0/item/%d.json" % story_id
            ).json()
            tweet = story["title"] + " " + story["url"]
        except Exception as e:
            print("**exception**", e)
            tweet = None
    return tweet


def main():
    tweet = hacker_news()
    print(tweet)
    if tweet:
        api.update_status(tweet)


if __name__ == "__main__":
    main()
