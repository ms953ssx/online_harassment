import sqlite3

conn = sqlite3.connect('tweets.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE TWEETS 
            (TWEETID INT(11) PRIMARY KEY NOT NULL,
            USERID VARCHAR(255),
            TWEET TEXT NOT NULL,
            ISHARASSMENT Boolean);''')

print ("Table created successfully")

conn.close()
