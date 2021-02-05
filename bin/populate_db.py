import os
import tweepy as tw
import pandas as pd
from elasticsearch import Elasticsearch
from datetime import datetime

consumer_key = os.environ.get("CONSUMER_KEY")  # Add your API key here
consumer_secret = os.environ.get("CONSUMER_SECRET")  # Add your API secret key here
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

es = Elasticsearch()


def get_tweets(search_term, date_since):
    tweets = tw.Cursor(api.search, q=search_term, lang="en", since=date_since).items(15)
    return tweets

def post_elastic(tweet_id, content):
    res = es.index(index="test-index", id=tweet_id, body=content)
    print(res['result'])

def store_id(tweet_id):
    f = open("tweet_ids.txt", "a")
    f.write(str(tweet_id))
    f.write("\n")
    f.close()

def main(): 
    tweets = get_tweets("Maradona", "2021-01-01")
    for tweet in tweets:
        store_id(tweet.id)
        post_elastic(tweet.id, tweet._json)

if __name__ == "__main__":
    main()
