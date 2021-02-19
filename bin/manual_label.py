import sqlite3

def main():
    
    conn = sqlite3.connect("tweets.db")

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(USERID) FROM TWEETS WHERE ISHARASSMENT IS NOT NULL")
        print(cur.fetchall())
        cur.execute("SELECT * FROM TWEETS WHERE USERID NOT IN (SELECT USERID FROM TWEETS ORDER BY RANDOM() LIMIT 200)")

        for tweet in cur.fetchall():
            tweet_id, user_id, tweet_txt, is_harassment = tweet
            print(tweet_txt, is_harassment)
            x = "blank"
            while x.lower() != 'y' and x.lower() != 'n':
                x = input("Is this harassment? Y/N: ")
                if x.lower() == 'y':
                    lbl = 1
                elif x.lower() == 'n':
                    lbl = 0
                else:
                    print("invalid input")
            sql = '''UPDATE TWEETS
                     SET ISHARASSMENT = ?
                     WHERE TWEETID = ? '''
            print(sql)
            cur.execute(sql, (lbl, tweet_id))
            conn.commit()




if __name__ == "__main__":
    main()
