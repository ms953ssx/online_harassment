import sqlite3

conn = sqlite3.connect('tweets.db')
print ("Opened database successfully")

conn.execute('''DELETE FROM TWEETS WHERE
        TWEET LIKE '%batty%' ''')

print ("FIELDS DELETED SUCCESSFULLY")

conn.close()
