"""
This file contains the main functions to access Twitter.
In order to see sample calls to these functions, refere to
example.py and test_twitter.py

The class Twitter provides methods to communicate with Twitter.
These are based on end points provided by

-Rakshit Agrawal, 2016
"""
import os
import unittest
import datetime
import requests
from pprint import pprint
from requests_oauthlib import OAuth1
from twitter_public_api import URL

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S"


def _timenow():
    return datetime.datetime.utcnow().strftime(DATE_FORMAT)


class Twitter(object):
    """
    Class for Twitter action functions.

    Functions in this class need tokens from twitter.
    User needs to sign up with an account on twitter and
    then generate the required tokens.

    https://dev.twitter.com/oauth/overview/application-owner-access-tokens

    """

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialize the authentication paramters
        Calls to twitter will not succeed in the absence of any parameter

        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def _auth(self):
        """
        Provide the OAuth signature using user app credentials
        :return: oauth signature
        """
        return OAuth1(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)

    def get_account_settings(self, **args):
        """
        Get settings for user account.

        (Under construction)

        :return:Dictionary of settings provided by Twitter
        :rtype: dict
        """
        url = URL['account_settings']
        settings = requests.get(url=url, auth=self._auth())

        if settings.status_code == requests.codes.ok:
            return settings.json()

    def get_user_timeline(self, user, using_id=False, count=10):
        """
        Get timeline for user specified by the user parameter.
        Can use either user's screen_name or user_id

        :param user: screen_name (twitter handle) or user_id for the user. user_id will be used only if use_id is set to True
        :type user: str
        :param use_id: Use the User ID if this value is set to True. Default is False
        :type use_id: bool
        :param count: Number of tweets to fetch from the timeline
        :type count: int
        :return: List of tweets on user timeline starting from latest
        :rtype: list
        """
        url = URL['user_timeline']
        if using_id:
            params = dict(user_id=user)
        else:
            params = dict(screen_name=user)

        params['count'] = count

        timeline = requests.get(url=url, auth=self._auth(), params=params)

        if timeline.status_code == requests.codes.ok:
            return timeline.json()

    def post_media(self, media_list):
        """
        Post media on twitter.
        Follows the Media API by twitter (https://dev.twitter.com/rest/media)

        This function is used by post_twitter for uploading media

        :param media_list: List of media file names (relative paths)
        :type media_list: list
        :return: List of media upload dicts
        :rtype: list
        """

        media_url = URL['media_upload']
        media_dicts = []

        for item in media_list:
            with open(item, 'rb') as mediafile:
                # Upload media to Twitter and get its ID
                media = requests.post(url=media_url, files=dict(media=mediafile), auth=self._auth())

            if media.status_code == requests.codes.ok:
                media_dicts.append(media.json())
        return media_dicts

    def post_tweet(self, text, media=None, latlong=None):
        """
        Post a tweet.
        A tweet can contain
            - only text
            - text and location
            - text, media and location

        Based on https://dev.twitter.com/rest/reference/post/statuses/update

        :param text: Tweet text
        :type text: str
        :param media: List of media items to be added with tweet
        :type media: list
        :param latlong: Tuple with latitutde and longitude in the format (latitude, longitude).
        This feature will only work if location settings are turned on for the user account. To set them on, go to https://twitter.com/settings/security
        In the Security and privacy tab, select the Tweet location feature to turn it on.
        :type latlong: tuple
        :return: JSON response from twitter
        :rtype: dict
        """
        url = URL['post_tweet']
        params = dict(status=text)

        # Upload media to Twitter if any
        if media is not None:
            media_dicts = self.post_media(media)
            params['media_ids'] = ",".join([i.get('media_id_string') for i in media_dicts])

        # Add location if provides
        if latlong is not None:
            params['lat'], params['long'] = latlong

        print params

        # Post tweet
        tweet = requests.post(url=url, auth=self._auth(), params=params)

        if tweet.status_code == requests.codes.ok:
            return tweet.json()

    def delete_tweet(self, tweet_id):
        """
        Delete tweet with the tweet ID
        Tweet ID should belong to a tweet by the user signed up with Access Tokens

        :param tweet_id: ID of tweet to be deleted
        :type tweet_id: int
        :return:
        :rtype:
        """
        url = URL['destroy_tweet'] % (tweet_id)
        deleted_tweet = requests.post(url=url, auth=self._auth())

        return deleted_tweet.json()
