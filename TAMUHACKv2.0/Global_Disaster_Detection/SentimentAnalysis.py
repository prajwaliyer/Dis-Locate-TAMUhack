#Importing libraries
import sys
import os
import jsonpickle
import tweepy
import csv
from textblob import TextBlob
from git import Repo
from itertools import groupby
from operator import itemgetter

def get_top_locations(grouped_by_location, cleanedTweets):
    top_location_indices = []
    top_locations = []
    while len(top_location_indices) < 3:
        max_count = 0
        max_index = 0

        #find the index with the most tweets
        for group in grouped_by_location:
            if grouped_by_location.index(group) not in top_location_indices:
                if len(group) > max_count:
                    max_count = len(group)
                    max_index = grouped_by_location.index(group)
        #update top location lists
        top_location_indices.append(max_index)
        tweet_dict = {t[0]:t[1:] for t in cleanedTweets}
        top_locations.append(tweet_dict[grouped_by_location[max_index][0]])
    return top_locations

def auth_tweepy():
    consumer_key = 'VBo9qa8ftO61mhSaYxHd6XHSn'

    consumer_secret = '9IqWfyO8TPeo4xj8fSaKMsJji5LbQh6JZWvOBbNpxvPLDFTOem'

    access_token = '2828468661-MRhcCGtBTOiBiRJlL0x4q6torL1WMm6leZjuaVH'

    access_secret = '7SgCleNBDZfWPGQNmKlmWNF2DX3wXaYFCVJ2JCdtqUiR9'
    #Pass our consumer key and consumer secret to Tweepy's user authentication handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #Pass our access token and access secret to Tweepy's user authentication handler
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    #Error handling
    if (not api):
        print ("Problem connecting to API")
    #Switching to application authentication
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #Setting up new api wrapper, using authentication only
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    #Error handling
    if (not api):
        print ("Problem Connecting to API")
    return api

api = auth_tweepy()
disaster = 'power outage'
searchQuery = disaster
maxTweets = 1000
tweetsPerQry = 100

csvFile = open('result.csv', 'w')

with open('CollectedTweets.json', 'w') as f:
    #Tell the Cursor method that we want to use the Search API (api.search)
    #Also tell Cursor our query, and the maximum number of tweets to return
    average = 0
    tweets = tweepy.Cursor(api.search,q=searchQuery).items(maxTweets)
    cleanedTweets = []
    tweetCount = 0
    for tweet in tweets:
        if tweet.place:#if tweet has location data
            cleanedTweets.append([tweet.text, tweet.place.full_name])
            #Write the JSON format to the text file, and add one to the number of tweets we've collected
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

    #group tweets by location
    cleanedTweets.sort(key = itemgetter(1))
    groups = groupby(cleanedTweets, itemgetter(1))
    grouped_by_location = [[item[0] for item in data] for (key, data) in groups]

    top_locations = get_top_locations(grouped_by_location, cleanedTweets)

    print(cleanedTweets)
    print(top_locations)
    #Display how many tweets we have collected
    print("Downloaded {0} tweets".format(tweetCount))
