import sqlite3

def main():
    
    conn = sqlite3.connect("tweets.db")

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(USERID) FROM TWEETS WHERE ISHARASSMENT IS NOT NULL")
        count = cur.fetchall()[0][0]
        cur.execute("SELECT * FROM TWEETS WHERE ISHARASSMENT IS NULL ORDER BY RANDOM() LIMIT 200")

        for tweet in cur.fetchall():
            tweet_id, user_id, tweet_txt, is_harassment = tweet
            print("Num of labelled tweets:", count)
            print(tweet_txt, is_harassment)
            x = "blank"
            while x.lower() != 'y' and x.lower() != 'n':
                x = input("\nIs this harassment? Y/N: ")
                if x.lower() == 'y':
                    lbl = 1
                elif x.lower() == 'n':
                    lbl = 0
                else:
                    print("\ninvalid input\n")
            sql = '''UPDATE TWEETS
                     SET ISHARASSMENT = ?
                     WHERE TWEETID = ? '''
            cur.execute(sql, (lbl, tweet_id))
            conn.commit()
            count +=1




if __name__ == "__main__":
    main()
