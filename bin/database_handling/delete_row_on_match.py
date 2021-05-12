#Used for removing tweets from database via sql query, later now unused
import sqlite3

conn = sqlite3.connect('../../etc/database_store/new_tweets_2.db')
print ("Opened database successfully")

conn.execute('''DELETE FROM TWEETS WHERE
        TWEET LIKE '%batty%' ''')

print ("FIELDS DELETED SUCCESSFULLY")

conn.close()
