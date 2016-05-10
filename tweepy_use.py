"""
Not Using this file !!


This file provides main interface to the API for Twitter interaction.


- Rakshit Agrawal, 2016
"""

import tweepy

class Tweet(object):
    """
    Twitter class for operations with twitter.
    Uses tweepy
    """

    def __init__(self):
        self.CONSUMER_KEY = None
        self.CONSUMER_SECRET = None

    def set_credentials(self, from_file=True):
        """

        :param from_file: Use credentials from credentials.py
        :type from_file: bool
        :return:
        :rtype:
        """
        if from_file:
            from credentials import CONSUMER_KEY, CONSUMER_SECRET
            self.CONSUMER_KEY = CONSUMER_KEY
            self.CONSUMER_SECRET = CONSUMER_SECRET

    def authorize(self):
        """
        Authorize the account for twitter access
        :return:
        :rtype:
        """
        self.set_credentials()
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)


        try:
            redirect_url = auth.get_authorization_url()
            print redirect_url
            print "Authorization successful"
        except tweepy.TweepError:
            print 'Error! Failed to get request token.'

        # Get access token
        # auth.get_access_token("verifier_value")

        # Construct the API instance
        api = tweepy.API(auth)

if __name__=="__main__":
    t = Tweet()
    t.authorize()