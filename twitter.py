"""
This file contains access to Twitter from a single account using token

"""
import requests
from pprint import pprint
from requests_oauthlib import OAuth1

URL = {
    'user_timeline': "https://api.twitter.com/1.1/statuses/user_timeline.json",
    'search': "https://api.twitter.com/1.1/search/tweets.json",
    'post_tweet': "https://api.twitter.com/1.1/statuses/update.json",
    'media_upload': "https://upload.twitter.com/1.1/media/upload.json",
}


class TwitterActions(object):
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

    def post_tweet(self, text, media=None):
        """
        Post a tweet

        Based on https://dev.twitter.com/rest/reference/post/statuses/update

        :param text: Tweet text
        :type text: str
        :param media: List of media items to be added with tweet
        :type media: list
        :return: JSON response from twitter
        :rtype: dict
        """
        url = URL['post_tweet']

        # Upload media to Twitter if any
        if media is not None:
            media_url = URL['media_upload']
            media_ids = []

            for item in media:
                with open(item, 'rb') as mediafile:
                    # Upload media to Twitter and get its ID
                    media = requests.post(url=media_url, files=dict(media=mediafile), auth=self._auth())

                if media.status_code == requests.codes.ok:
                    media_ids.append(media.json().get('media_id'))

            # Post the tweet with media
            tweet = requests.post(url=url, auth=self._auth(), params=dict(status=text, media_ids=media_ids))

        else:
            # Post a tweet without media
            tweet = requests.post(url=url, auth=self._auth(), params=dict(status=text))

        return tweet.json()


if __name__ == "__main__":

    from credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

    twitter = TwitterActions(consumer_key=CONSUMER_KEY,
                             consumer_secret=CONSUMER_SECRET,
                             access_token=ACCESS_TOKEN,
                             access_token_secret=ACCESS_TOKEN_SECRET)

    media_list = ['m01.jpg','m02.jpg','m03.jpg']
    text = "Random pictures from pixabay"

    tweet1 = twitter.post_tweet(text=text, media=media_list)

    text2 = "Another tweet without any media"

    tweet2 = twitter.post_tweet(text2)

    pprint(tweet1)
    pprint(tweet2)