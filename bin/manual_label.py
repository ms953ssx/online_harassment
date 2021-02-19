import sqlite3

def main():
    
    conn = sqlite3.connect("tweets.db")

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(USERID) FROM TWEETS WHERE ISHARASSMENT IS NOT NULL")
        count = cur.fetchall()[0][0]
        cur.execute("SELECT * FROM TWEETS WHERE ISHARASSMENT IS NULL ORDER BY RANDOM() LIMIT 200")

        for tweet in cur.fetchall():
            tweet_id, user_id, tweet_txt, is_type_homosexual, is_type_transgender, is_type_bisexual, is_harassment = tweet
            print("\nNum of labelled tweets:", count)
            print("\n\nTweet ID: ", tweet_id, "\nTweet Content: ", tweet_txt, "\nCurrent label: ", is_harassment)
            x = "blank"
            while x.lower() != 'y' and x.lower() != 'n' and x.lower() != 'd':
                x = input("\nIs this harassment? Y/N: ")
                if x.lower() == 'y':
                    lbl = 1
                elif x.lower() == 'n':
                    lbl = 0
                elif x == "?":
                    break
                elif x.lower() == 'd':
                    lbl = 2
                else:
                    print("\ninvalid input\n")
            if x == "?":
                continue
            if lbl == 2:
                sql = ''' DELETE FROM TWEETS WHERE TWEETID = ? '''
                cur.execute(sql, (tweet_id,))
                conn.commit()
                print("\nTweet successfully deleted from database")
            else:    
                sql = '''UPDATE TWEETS
                         SET ISHARASSMENT = ?
                         WHERE TWEETID = ? '''
                cur.execute(sql, (lbl, tweet_id))
                conn.commit()
                print("\nTweet successfully updated in database")
                count +=1





if __name__ == "__main__":
    main()
