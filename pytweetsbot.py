import tweepy
import time
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(
    consumer_key, consumer_secret
)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
user = api.me()
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

#print(user.name)


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(1000)


# for follower in limit_handler(tweepy.Cursor(api.followers).items()):
#     print(follower.name)

query_string = '#COVID19'
no_of_tweets = 2

for tweet in tweepy.Cursor(api.search, query_string).items(no_of_tweets):
    try:
        tweet.retweet()
        print('Retweeted it')
        tweet.favorite()
        print('Liked it')

    except tweepy.TweepError as err:
        print(err.reason)

    except StopIteration:
        break
