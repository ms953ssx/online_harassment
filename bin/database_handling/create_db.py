import sqlite3

conn = sqlite3.connect('../../etc/database_store/new_tweets_2.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE TWEETS 
            (TWEETID INT(11) PRIMARY KEY NOT NULL,
            USERID VARCHAR(255) NOT NULL,
            TWEET VARCHAR(255) NOT NULL,
            ISTYPEHOMOSEXUAL Boolean,
            ISTYPETRANSGENDER Boolean,
            ISTYPEBISEXUAL Boolean,
            HASPRONOUNS Boolean,
            ISHARASSMENT Boolean);''')

print ("Table created successfully")

conn.close()
