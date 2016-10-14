##########################################################
# First Populate of the db (Run this only first time!)
##########################################################

import settings
from common import insert_all_tweets

if __name__ == '__main__':
    insert_all_tweets(settings.TARGET_USR)
