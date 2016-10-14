import tweepy

from random import random

from pymongo import MongoClient, DESCENDING

from settings import *


def mongo_connector():
    client = MongoClient(MONGO_CLIENT)
    db = client[MONGO_DB_NAME]
    db.authenticate(AUTH_USR, AUTH_PWD)

    return db


def tweepy_connector():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

db  = mongo_connector()
api = tweepy_connector()


def insert_tweets(tweet_list):
    tweets = []

    for t in tweet_list:
        if t.in_reply_to_screen_name is None:
            print 'inserting tweets'
            tweets.append(t)
            db.tweets.insert({
                'tweet_id': t.id,
                'text': t.text,
                'random': [random(), 0]}
            )

    return tweets


def insert_all_tweets(screen_name):

    print 'looking for tweets'

    recent = api.user_timeline(screen_name=screen_name, count=200)

    tweets = insert_tweets(recent)

    oldest = tweets[-1].id - 1

    while len(recent) > 0:
        print 'getting old tweets'

        recent = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        _ = insert_tweets(recent)

        oldest = tweets[-1].id - 1


def insert_latest_tweets(screen_name):

    last_tweet = list(db.tweets.find().sort('tweet_id', DESCENDING).limit(1))

    print 'looking for tweets'

    recent = api.user_timeline(screen_name=screen_name, count=200, since_id=last_tweet[0]['tweet_id'])

    if recent:
        _ = insert_tweets(recent)
    else:
        print 'no new tweets!'
