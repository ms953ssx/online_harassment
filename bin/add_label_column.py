import sqlite3

conn = sqlite3.connect('tweets.db')
print ("Opened database successfully")

conn.execute('''ALTER TABLE TWEETS
         ADD COLUMN AUTO_PASTEXPERIENCE Boolean;''')

print ("FIELD ADDED SUCCESSFULLY")

conn.close()
