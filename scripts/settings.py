# Settings file
import os

MONGO_CLIENT = None
MONGO_DB_NAME = 'twitter'

AUTH_USR = None
AUTH_PWD = None

CONSUMER_KEY     = None
CONSUMER_SECRET  = None

ACCESS_KEY       = None
ACCESS_SECRET    = None

TARGET_USR = None

HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 33507)
