# Twitter using Python #

This repository provides some functions to communicate with Twitter using API provided by Twitter.

The functions provided here require singe user token from Twitter which can be obtained from [https://dev.twitter.com/oauth/overview/application-owner-access-tokens](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)


* twitter.py provides main set of functions to operate the API
* tweepy_use.py has a broken implementation based on tweepy library
* Four credentials are required to use an application for accessing twitter on user's behalf

Create a file credentials.py in the same directory and set the credential in it as follows:

```python
CONSUMER_KEY = "Consumer Key from Twitter"
CONSUMER_SECRET = "Consumer Secret from Twitter"

ACCESS_TOKEN = "Access Token from Twitter"
ACCESS_TOKEN_SECRET = "Access token secret from Twitter"
```