import sqlite3

exceptions = ["1371601805445099520", "1370858546133340172","1365295656563339265","1371221382688874502"]
def main():
    
    conn = sqlite3.connect("tweets.db")
    with conn:
        for tweetid in exceptions:
            cur = conn.cursor()
            sql = '''SELECT * FROM TWEETS WHERE TWEETID = ? '''
            cur.execute(sql, (tweetid,))
            tweet = cur.fetchall()
            print(tweet)
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
                cur.execute(sql, (tweetid,))
                conn.commit()
                print("\nTweet successfully deleted from database")
            else:    
                sql = '''UPDATE TWEETS
                         SET ISHARASSMENT = ?
                         WHERE TWEETID = ? '''
                cur.execute(sql, (lbl, tweetid))
                conn.commit()
                print("\nTweet successfully updated in database")





if __name__ == "__main__":
    main()
