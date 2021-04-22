import sqlite3

conn = sqlite3.connect('tweets.db')
print ("Opened database successfully")

conn.execute('''ALTER TABLE TWEETS
        DROP AUTO_ISTHIRDPERSON,
        DROP ISTHIRDPERSON,
        DROP AUTO_ISSECONDPERSON,
        DROP ISSECONDPERSON,
        DROP AUTO_ISFIRSTPERSON,
        DROP ISFIRSTPERSON;''')

print ("FIELDS DROPPED SUCCESSFULLY")

conn.close()
