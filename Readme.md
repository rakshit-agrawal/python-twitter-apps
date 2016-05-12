# Twitter using Python #

This repository provides some functions to communicate with Twitter using API provided by Twitter.

The functions provided here require singe user token from Twitter which can be obtained from [https://dev.twitter.com/oauth/overview/application-owner-access-tokens](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)


* twitter.py provides main set of functions to operate the API
* Four credentials are required to use an application for accessing twitter on user's behalf

## Dependencies ##
This code uses Python [Requests](http://docs.python-requests.org/en/master/) library which is not provided by default Python installation 

Create a file credentials.py in the same directory and set the credential in it as follows:

```python
CONSUMER_KEY = "Consumer Key from Twitter"
CONSUMER_SECRET = "Consumer Secret from Twitter"

ACCESS_TOKEN = "Access Token from Twitter"
ACCESS_TOKEN_SECRET = "Access token secret from Twitter"

twitter_access = dict(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)

```