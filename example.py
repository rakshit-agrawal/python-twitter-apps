"""
This file is only for testing basic functions of the library.
It should be used only after writing credentials.py

-Rakshit Agrawal, 2016
"""
import datetime
import os
import time
from credentials import twitter_access, twitter_username
from twitter import Twitter

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S"
TWEET_TEXT = "Hello! This is a test tweet using https://github.com/rakshit-agrawal/python-twitter-apps at %r UTC."

t = Twitter(**twitter_access)

# Post a simple tweet
tweet1 = t.post_tweet(text=TWEET_TEXT % (datetime.datetime.utcnow().strftime(DATE_FORMAT)))

time.sleep(2)
# Post a tweet with location
ll = (37.000880, -122.062309)
tweet2 = t.post_tweet(text=TWEET_TEXT % (datetime.datetime.utcnow().strftime(DATE_FORMAT)),
                      latlong=ll)

time.sleep(2)
# Post a tweet with sample media JPEGS
jpegs = ['m01.jpg', 'm02.jpg']
media_list = [os.path.join('testing', i) for i in jpegs]
tweet_text = TWEET_TEXT % (datetime.datetime.utcnow().strftime(DATE_FORMAT)) + " Pictures from Pixabay."
tweet3 = t.post_tweet(text=tweet_text,
                      media=media_list)
