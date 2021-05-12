import sqlite3
import re
import pandas as pd
from spellchecker import SpellChecker
from wordsegment import load, segment
load()

def clean_data(df):
    l_clean_tweets = []
    for i,line in df.iterrows():
        print(i, "th tweet \nbase tweet: ", line.TWEET)
        tweet = preprocess(line.TWEET)
        l_clean_tweets.append(tweet)
        print("preprocessed tweet: ", tweet)
    return l_clean_tweets

def preprocess(tweet):
    tweet = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)','',tweet, flags=re.MULTILINE) # to remove links that start with HTTP/HTTPS in the tweet
    tweet = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '',tweet, flags=re.MULTILINE) # to remove other url links
    tweet = ' '.join(re.sub('([^0-9A-Za-z \t])|(\w+:\/\/\S+^@)','',tweet).split()) #remove # and emojis
    tweet = ' '.join(re.sub('(\r\n|\r|\n)|\.\.\.','',tweet).split()) #remove ellipsis and newlines as these seems to be an issue for wordsegment
    tweet = re.sub(r"\d", "", tweet)
    spell = SpellChecker()
    tweet = ' '.join([spell.correction(w) for w in tweet.split()]) #correct spelling errors
    tweet = tweet.lower()
    return tweet
    
def remove_bad_columns(db):
    db.drop("ISFIRSTPERSON", inplace=True, axis=1)
    db.drop("ISSECONDPERSON", inplace=True, axis=1)
    db.drop("ISTHIRDPERSON", inplace=True, axis=1)
    db.drop("AUTO_ISFIRSTPERSON", inplace=True, axis=1)
    db.drop("AUTO_ISSECONDPERSON", inplace=True, axis=1)
    db.drop("AUTO_THIRDPERSON", inplace=True, axis=1)
    return db

def get_old_db():
    conn = sqlite3.connect("../../etc/database_store/new_tweets_2.db")
    with conn:
        cur = conn.cursor()
        old_db = pd.read_sql(con=conn,sql="SELECT * FROM TWEETS")
    return old_db

def put_new_db(db):
    conn = sqlite3.connect("../../etc/database_store/new_tweets_3.db")
    db.to_sql("TWEETS", conn, if_exists="append",index=False)
    print("successfully put new db!")

def main():
    old_db = get_old_db()
    new_db = remove_bad_columns(old_db)
    new_db['CLEAN_TWEET'] = clean_data(new_db)
    put_new_db(new_db)
    
    #iterate rows and preprocess each tweet, storing under clean_tweets

if __name__ == "__main__":
    main()
