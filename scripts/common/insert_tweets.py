

def get_specific(tweet_list):
	for t in tweet_list:
		if t.in_reply_to_screen_name is None:
			print 'inserting tweets'
			tweets.append(t)	
			db.tweets.insert({
				'tweet_id': t.id, 
				'text': t.text, 
				'random': [random(), 0]})