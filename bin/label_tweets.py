import os
import tweepy as tw
from elasticsearch import Elasticsearch
import json
import numpy
from snorkel.labeling import labeling_function
from snorkel.labeling import LFApplier
from snorkel.labeling import LFAnalysis

es = Elasticsearch()

ABSTAIN = -1
SAFE = 0
DEATH = 1


@labeling_function()
def rip(x):
    # Return a label of DEATH if "RIP" in comment text, otherwise ABSTAIN
    return DEATH if "rip" in x['full_text'].lower() else ABSTAIN

@labeling_function()
def rest_in_peace(x):
    # Return a label of DEATH if "RIP" in comment text, otherwise ABSTAIN
    return DEATH if "rest in peace" in x['full_text'].lower() else ABSTAIN

@labeling_function()
def died(x):
    return DEATH if "died" in x['full_text'].lower() else ABSTAIN

@labeling_function()
def dead(x):
    return DEATH if "dead" in x['full_text'].lower() else ABSTAIN

def perf_eval(input_dict, lfs):
    return LFAnalysis(L=input_dict, lfs=lfs).lf_summary()


def main(): 
    #instantiate labelling functions
    lfs = [rip, died, dead]
    applier = LFApplier(lfs=lfs)
    #Store dict of tweets to labelling function output for performance analysis
    tweet_dict = {}
    #Open tweet ID file of already stored database entries
    file1 = open("tweet_ids.txt", "r")
    Lines = file1.readlines()
    #Iterate through newline delineated list of stored tweet ids
    for line in Lines:
        
        #Strip newline character
        tweet_id = line.strip()
        
        #Search ID in elastic query to retrieve json output
        tweet = es.get(index="test-index", id=tweet_id)

        #Get just tweet content stored in a nested dictionary
        tweet_json = tweet['_source']
        
        #Run through snorkel labelling function on tweet content
        classify = applier.apply([tweet_json])
        tweet_dict[tweet_json['full_text']] = classify
        
        #Output tweet content with output of labeling function for manual review
        print(tweet_json['full_text'], classify)
        
        #Update elastic database with labelled tweet
        #post_elastic(classify, tweet, tweet_id)

    #Produce performance evaluation metrics to see coverage of our labeling functions
    print(perf_eval(numpy.concatenate(list(tweet_dict.values())),lfs))

if __name__ == "__main__":
    main()


