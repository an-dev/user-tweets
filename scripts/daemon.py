###########################################
# Daemon to populate the db periodically
###########################################

import settings
from common import insert_latest_tweets

if __name__ == '__main__':
    insert_latest_tweets(settings.TARGET_USR)
