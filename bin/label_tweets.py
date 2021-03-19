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
l_names_or_places = r"(van dyke|ponce de leon|ponce city|ponce inlet town)" 
@labeling_function()
def names_or_places(tweet_text):
    return NEGATIVE if re.search(l_famous_names, tweet_text.lower()) else ABSTAIN

#Common simple insults
l_simple_insults = r"(fucking|disgusting|ugly|bitchy|pathetic) (fag|faggot|fags|fudgepacker|fudge packer|poofter|pansy|bender|batty boy|ponce|dyke|rug muncher|lesbo|tranny|trannie|transvestite|ladyboy|heshe|shemale|switch hitter)"
@labeling_function()
def simple_insults(tweet_text):
    return POSITIVE if re.search(l_simple_insults, tweet_text.lower()) else ABSTAIN

#Common terms used to identify the subject of a given bad term e.g. "You ***" 
l_term_to_person = r"(that|this|you|shut the fuck up|stfu) (fag|faggot|fags|fudgepacker|fudge packer|poofter|pansy|bender|batty boy|ponce|dyke|rug muncher|lesbo|tranny|trannie|transvestite|ladyboy|heshe|shemale|switch hitter)"
@labeling_function()
def term_to_person(tweet_text):
    return POSITIVE if re.search(l_term_to_person, tweet_text.lower()) else ABSTAIN

#Using term in a descriptive yet derogatory manner
l_descriptive_bad = r"(piece of|like a) (fag|faggot|fags|fudgepacker|fudge packer|poofter|pansy|bender|batty boy|ponce|dyke|rug muncher|lesbo|tranny|trannie|transvestite|ladyboy|heshe|shemale|switch hitter)"
@labeling_function()
def descriptive_bad(tweet_text):
    return POSITIVE if re.search(l_descriptive_bad, tweet_text.lower()) else ABSTAIN

#Stating someone on the LGBT spectrum is unnatural
l_against_nature = r"(against|defying) (god|biology|nature)"
@labeling_function()
def against_nature(tweet_text):
    return POSITIVE if re.search(l_against_nature, tweet_text.lower()) else ABSTAIN


#Contains trigger warning
l_trigger_warnings = r"(\/+ *tw|\/* *trigger warning)"
@labeling_function()
def trigger_warning(tweet_text):
    return NEGATIVE if re.search(l_trigger_warnings, tweet_text.lower()) else ABSTAIN

#Using term 'Bender' when talking about drunken stints
l_bender_as_drunk = r"(day|on a) bender"
@labeling_function()
def bender_as_drunk(tweet_text):
    return NEGATIVE if re.search(l_bender_as_drunk, tweet_text.lower()) else ABSTAIN

#Using Bender as a pop culture reference e.g. avatar the last airbender or Futurama reference
l_bender_pop_culture = r"((fender|water|earth|fire|wind|energy) *bender)|futurama.*bender|bender.*futurama|avatar.*bender"
def bender_pop_culture(tweet_text):
    return NEGATIVE if re.search(l_bender_pop_culture, tweet_text.lower()) else ABSTAIN

#Using slang term for using cigarettes
l_slang_using_cigarettes = r"((for|smoke|have|smoking|having) (some|a) fags?)|fag ash"
def slang_using_cigarettes(tweet_text):
    return NEGATIVE if re.search(l_slang_using_cigarettes, tweet_text.lower()) else ABSTAIN

#Slur is part of a mentioned twitter handle
l_handles = r"(\@[a-z0-9_]*)"
def slur_in_handles(tweet_text):
    in_handle = 0
    bad_terms = ['fag', 'faggot', 'fags', 'fudgepacker', 'fudge+packer', 'poofter', 'pansy', 'bender', 'batty+boy', 'ponce', 'dyke', 'rug+muncher', 'lesbo','tranny', 'trannie', 'transvestite', 'ladyboy', 'heshe', 'shemale','switch+hitter', 'gay+for+pay']
    #check for slur in handle
    handles = re.findall(l_handles, tweet_text.lower())
    for handle in handles:
        if any(substring in handle for substring in bad_terms):
            in_handle+=1
    
    return NEGATIVE if in_handle>0 else ABSTAIN


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


