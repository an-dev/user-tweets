try:
    import gevent.monkey
    gevent.monkey.patch_all()
except:
    pass

import settings

from bottle import route, run, view, TEMPLATE_PATH, static_file
from scripts.common import mongo_connector

from random import random


db  = mongo_connector()

TEMPLATE_PATH.insert(0, './index.tpl')


@route('/static/<folder>/<filename>')
def server_static(folder, filename):
    return static_file(filename, root='./assets/{}'.format(folder))


@route('/')
@view('index')
def index():
    tweet = list(
        db.tweets.find({
            'random': {
                '$near': [random(), 0]
            }
        }).limit(1)
    )

    return dict(tweet=tweet[0]['text'])

run(server='gevent', host=settings.HOST, port=settings.PORT)
