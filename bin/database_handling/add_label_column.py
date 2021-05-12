import sqlite3

conn = sqlite3.connect('../../etc/database_store/new_tweets_2.db')
print ("Opened database successfully")

conn.execute('''ALTER TABLE TWEETS
         ADD COLUMN AUTO_PASTEXPERIENCE Boolean;''')

print ("FIELD ADDED SUCCESSFULLY")

conn.close()
