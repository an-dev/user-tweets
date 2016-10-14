###########################################
# Daemon to populate the db periodically
###########################################

import settings
from common import get_tweets

if __name__ == '__main__':
    get_tweets(settings.TARGET_USR)
