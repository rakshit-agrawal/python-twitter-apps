# Twitter API usage with Python
Rakshit Agrawal, 2016

This repository provides some basic functions to communicate with Twitter using [Public API](https://dev.twitter.com/rest/public) provided by Twitter.

## Dependencies
This code uses Python [Requests](http://docs.python-requests.org/en/master/) library which is not provided by default Python installation.
It also used [Request-OAuthlib](https://requests-oauthlib.readthedocs.io/en/latest/) for OAuth functions.


## Overview

The library provides following features at this stage:

- Get settings of the user account
- Get the user's timeline
- Post a tweet (plain, with location, and with media)
- Delete a specific tweet


## Getting Started

The function provided by this repository require authentication tokens from Twitter. In order to obtain the tokens, follow the steps:

* Create a [twitter](https://twitter.com/) account you plan to use. Any tweet sent through this API will reflect on this user's timeline.
* Create an App through [this link](https://apps.twitter.com/).
* Obtain the authentication parameters for your App by following [steps](https://dev.twitter.com/oauth/overview/application-owner-access-tokens) provided by Twitter. 
* You need to obtain Consumer Key, Consumer Secret, Access Token, and Access Token Secret
* An easy way to store and use these files while accessing the functions is to create a file credentials.py store the settings in it as follows:
    
    ```python
    CONSUMER_KEY = "Consumer Key from Twitter"
    CONSUMER_SECRET = "Consumer Secret from Twitter"
    
    ACCESS_TOKEN = "Access Token from Twitter"
    ACCESS_TOKEN_SECRET = "Access token secret from Twitter"
    
    twitter_access = dict(consumer_key=CONSUMER_KEY,
                          consumer_secret=CONSUMER_SECRET,
                          access_token=ACCESS_TOKEN,
                          access_token_secret=ACCESS_TOKEN_SECRET)
                     
    twitter_username = "Username for Twitter account"
    ```
* Once you have the value, you can start using the library

    ```python
    from credentials import twitter_access, twitter_username
    from twitter import Twitter   
     
    t = Twitter(**twitter_access)
    
    # To post a tweet
    t.post_tweet(text="Hello World")
    
    ```
* Once you have the credentials ready, you can also run example.py to post some sample tweets
