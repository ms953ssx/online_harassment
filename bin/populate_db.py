import os
import tweepy as tw
import pandas as pd
import csv
import sqlite3
from datetime import datetime

consumer_key = os.environ.get("CONSUMER_KEY")  # Add your API key here
consumer_secret = os.environ.get("CONSUMER_SECRET")  # Add your API secret key here
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

bad_words = ['queer', 'gimp', 'slut', 'whore', 'fag', 'faggot', 'fags', 'fudgepacker', 'fudge+packer', 'poof','poofter', 'pansy', 'sissy', 'bender', 'batty', 'ponce', 'jiggalo', 'dyke', 'rug+muncher', 'lesbo', 'tranny', 'trannie', 'transvestite', 'ladyboy', 'trap', 'HeShe', 'shemale', 'switch+hitter']

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


def main(): 
    conn = sqlite3.connect('tweets.db')
    print("Opened Database successfully")
    
    query = " OR ".join(bad_words) + " exclude:retweets"
    with conn:
        for tweet in tw.Cursor(api.search,
                                   q = query,
                                   lang = "en",
                                   tweet_mode='extended').items(2500):
            sql = '''
                INSERT OR REPLACE INTO TWEETS(TWEETID, USERID, TWEET) \
                VALUES (?,?,?)
                '''
            cur = conn.cursor()
            cur.execute(sql, (tweet.id, tweet.user.id, tweet.full_text.encode('utf-8')))
            conn.commit()
            print(tweet.id, tweet.user.id, tweet.full_text)

if __name__ == "__main__":
    main()
