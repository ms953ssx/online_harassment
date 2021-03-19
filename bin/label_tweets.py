import os
import re
import tweepy as tw
import json
import numpy as np
from snorkel.labeling import labeling_function
from snorkel.labeling import LFApplier
from snorkel.labeling import LFAnalysis
from sklearn import svm
import sqlite3


NEGATIVE = 2
ABSTAIN = 0
POSITIVE = 1

#Common names that have been found in dataset
famous_names = r"\b(Van dyke| Ponce de Leon)" 
@labeling_function()
def famous_names(tweet_text):
    return NEGATIVE if re.search(famous_names, tweet_text.lower()) else ABSTAIN

#Common simple insults
simple_insults = r"\b(fucking|disgusting|ugly) (fag|faggot|fags|fudgepacker|fudge packer|poofter|pansy|bender|batty boy|ponce|dyke|rug muncher|lesbo|tranny|trannie|transvestite|ladyboy|heshe|shemale|switch hitter)"
@labeling_function()
def simple_insults(tweet_text):
    return POSITIVE if re.search(simple_insults, tweet_text.lower()) else ABSTAIN


def perf_eval(input_dict, lfs):
    return LFAnalysis(L=input_dict, lfs=lfs).lf_summary()


def make_Ls_matrix(data, LFs):
    noisy_labels = np.empty((len(data), len(LFs)))
    for k, v in data.items():
        for j, lf in enumerate(LFs):
            noisy_labels[(k, v)][j] = lf(row)
    return noisy_labels




#def train(input_dict, classifier):
 #   clf = svm.SVC(gamma=0.001, C=100.)
  #  clf.fit(input_dict.values(), 
   # return classifier


def main(): 
    #instantiate labelling functions
    lfs = [famous_names, ]
    applier = LFApplier(lfs=lfs)
    #Store dict of tweets to labelling function output for performance analysis
    tweet_dict = {}
    #Connect to DB
    conn = sqlite3.connect("tweets.db")
    #Retrieve Tweets from Database
    with conn:
        cur = conn.cursor()
        #Construct SQL Queries
        #Obtain all manually labelled tweets from DB
        cur.execute("SELECT * FROM TWEETS WHERE ISHARASSMENT IS NOT NULL ORDER BY RANDOM()")
        lab_tweets = cur.fetchall()
    #Create train test split
    train, test = train_test_split(lab_tweets, test_size=0.33, random_state=42)
    
    #Tweets contain following fields in order:
    #twid, uid, tweet, is_homophobic, is_transphobic, is_biphobic, has_pronouns, is_harassment, auto_is_harassment   
    
    #Run through snorkel labelling function on tweet content
    classify = applier.apply(train)
    
        
    #Output tweet content with output of labeling function for manual review
    print(train, classify)
        
        
    #Build a matrix of LF votes for each tweet
    LF_Matrix = make_Ls_matrix(tweet_dict, classify)
    Y_LF_set = np.array(LF_set['label'])

    display(lf_summary(sparse.csr_matrix(LF_Matrix), Y=Y_LF_set, lf_names=LF_names.values()))

    #Produce performance evaluation metrics to see coverage of our labeling functions
    print(perf_eval(np.concatenate(list(tweet_dict.values())),lfs))

if __name__ == "__main__":
    main()


