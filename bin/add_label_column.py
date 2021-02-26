import sqlite3

conn = sqlite3.connect('tweets.db')
print ("Opened database successfully")

conn.execute('''ALTER TABLE TWEETS
        ADD HASPRONOUNS Boolean;''')

print ("FIELD UPDATED SUCCESSFULLY")

conn.close()
