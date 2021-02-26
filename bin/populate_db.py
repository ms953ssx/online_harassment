import os
import tweepy as tw
import pandas as pd
import csv
import sqlite3
from datetime import datetime
import itertools

consumer_key = os.environ.get("CONSUMER_KEY")  # Add your API key here
consumer_secret = os.environ.get("CONSUMER_SECRET")  # Add your API secret key here
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

homosexual_terms = ['fag', 'faggot', 'fags', 'fudgepacker', 'fudge+packer', 'poofter', 'pansy', 'bender', 'batty', 'ponce', 'dyke', 'rug+muncher', 'lesbo']
transgender_terms = ['tranny', 'trannie', 'transvestite', 'ladyboy', 'HeShe', 'shemale']
bisexual_terms = ['switch+hitter', 'gay+for+pay']

#List of pronouns for identification in bio
pronouns = ["he","she", "him", "her", "his", "hers", "them", "their", "they"]
cart_pronouns = itertools.product(pronouns, pronouns)
pronoun_list = []
for pronoun_prod in cart_pronouns:
    pronoun_list.append("/".join(pronoun_prod))

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

    query = " OR ".join(homosexual_terms) + " OR ".join(transgender_terms) + " OR ".join(bisexual_terms) + " exclude:retweets"
    count = 0
    with conn:
        try:
            for tweet in tw.Cursor(api.search,
                                   q = query,
                                   lang = "en",
                                   tweet_mode="extended",
                                   since="2020-02-20").items(900):

                #Check if tweet content contains word from bad terms lists
                is_type_homosexual = 0
                is_type_transgender = 0
                is_type_bisexual = 0
                has_pronouns = 0
                if any(word in tweet.full_text for word in homosexual_terms):
                    is_type_homosexual = 1
                if any(word in tweet.full_text for word in transgender_terms):
                    is_type_transgender = 1
                if any(word in tweet.full_text for word in bisexual_terms):
                    is_type_bisexual = 1
                if any(word in tweet.user.description for word in pronoun_list):
                    has_pronouns = 1
                sql = '''
                    INSERT OR REPLACE INTO TWEETS(TWEETID, USERID, TWEET, ISTYPEHOMOSEXUAL, ISTYPETRANSGENDER, ISTYPEBISEXUAL, HASPRONOUNS) \
                    VALUES (?,?,?,?,?,?,?)
                    '''
                cur = conn.cursor()
                cur.execute(sql, (tweet.id, tweet.user.id, tweet.full_text, is_type_homosexual, is_type_transgender, is_type_bisexual, has_pronouns))
                conn.commit()
                print(tweet.id, tweet.user.id, tweet.full_text, is_type_homosexual, is_type_transgender, is_type_bisexual, has_pronouns)
                count+=1
        except tw.TweepError as err:
            print(err)

        print("Stored: ", count, " tweets.")

if __name__ == "__main__":
    main()
