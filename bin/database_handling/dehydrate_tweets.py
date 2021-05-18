#Obtain hydrated database
import sqlite3
import pandas as pd
import tweepy as tw
import os

#Retrieve storage to double check if stored correctly
#Connect to DB
conn = sqlite3.connect("../../etc/database_store/auto_tweets_2.db")
#Retrieve Tweets from Database
with conn:
    cur = conn.cursor()
    #Construct SQL Queries
    #Obtain all manually labelled tweets from DB
    auto_data = pd.read_sql(con=conn,sql="SELECT * FROM TWEETS")

def dehydrate(hydrated_pd):
    dehydrated_pd = hydrated_pd[["TWEETID", "HASPRONOUNS","ISHARASSMENT","AUTO_ISHARASSMENT"]]
    return dehydrated_pd

dehydrated = dehydrate(auto_data)

#Put newly dehydrated database to new store

conn = sqlite3.connect("../../etc/dehydrated_store/dehydrated_tweets.db")
dehydrated.to_sql("TWEETS", conn, if_exists="replace", index=False)
print("successfully put new db")
