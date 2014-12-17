#import json
###########################################
#	Daemon to populate the db periodically
###########################################
import tweepy
from pymongo import MongoClient, ASCENDING, DESCENDING
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
last_tweet = list(db.tweets.find().sort('tweet_id', DESCENDING).limit(1))

def get_specific(tweet_list):
	for t in tweet_list:
		if t.in_reply_to_screen_name is None:
			print 'inserting tweets'
			tweets.append(t)	
			db.tweets.insert({'tweet_id': t.id, 'text': t.text, 'random': [random(), 0]})
			#print json.dumps({'tweet_id': t.id, 'text': t.text}, indent=2, separators=(',', ': '))

def get_all_tweets(screen_name):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	print 'looking for tweets'

	'''print last_tweet[0]['tweet_id']
	print last_tweet[0]['text']'''

	recent = api.user_timeline(screen_name = screen_name,count=200,since_id=last_tweet[0]['tweet_id'])

	#print recent
	
	if recent:
		get_specific(recent)
	else:
		print 'no new tweets!'
	
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(settings.TARGET_USR)
