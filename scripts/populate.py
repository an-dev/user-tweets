#import json
##########################################################
#	First Populate of the db (Run this only first time!)
##########################################################
import tweepy
from pymongo import MongoClient
from random import random
from local import settings

client = MongoClient(settings.MONGO_CLIENT)
db = client.twitter
db.authenticate(settings.AUTH_USR, settings.AUTH_PWD)

CONSUMER_KEY=settings.CONSUMER_KEY
CONSUMER_SECRET=settings.CONSUMER_SECRET
ACCESS_KEY=settings.ACCESS_KEY
ACCESS_SECRET=settings.ACCESS_SECRET
tweets = []

def get_specific(tweet_list):
	for t in tweet_list:
		if t.in_reply_to_screen_name is None:
			print 'inserting tweets'
			tweets.append(t)	
			db.tweets.insert({'tweet_id': t.id, 'text': t.text, 'random':[random(), 0]})
			#print json.dumps({'tweet_id': t.id, 'text': t.text}, indent=2, separators=(',', ': '))

def get_all_tweets(screen_name):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	print 'looking for tweets'

	recent = api.user_timeline(screen_name = screen_name,count=200)

	get_specific(recent)

	oldest = tweets[-1].id - 1
	
	while len(recent) > 0:

		print 'getting old tweets'
		
		recent = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		get_specific(recent)
		
		oldest = tweets[-1].id - 1

if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(settings.TARGET_USR)