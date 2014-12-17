try:
	import gevent.monkey
	gevent.monkey.patch_all()
except:
	pass
import os
from bottle import route, run, view, TEMPLATE_PATH, static_file
from pymongo import MongoClient
from random import random
from local import settings


client = MongoClient(settings.MONGO_CLIENT)
#client = MongoClient()
db = client.twitter
db.authenticate(settings.AUTH_USR, settings.AUTH_PWD)
TEMPLATE_PATH.insert(0, './index.tpl')


@route('/static/<folder>/<filename>')
def server_static(folder,filename):
    return static_file(filename, root='./assets/{}'.format(folder))


@route('/')
@view('index')
def index():
    tweet = list(db.tweets.find({'random': {'$near': [random(), 0]}}).limit(1))
    return dict(tweet=tweet[0]['text'])

run(server='gevent', host='0.0.0.0', port=os.environ.get('PORT', 33507))
#run(host='localhost', port='8080')
