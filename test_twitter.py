import json
import unittest
import requests
import datetime
import os

from credentials import twitter_access, twitter_username
from twitter import Twitter

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S"

TEST_TWEETS = 'testing/test_tweets.json'
TOP_TWEET = 'testing/top_tweet_id_file.json'


def _timenow():
    return datetime.datetime.utcnow().strftime(DATE_FORMAT)


def _write_top_tweet_file(tweet_id):
    with open(os.path.join(os.getcwd(), TOP_TWEET), 'wb') as outfile:
        json.dump(dict(id=tweet_id), outfile)


def _read_id_top_tweet():
    if os.path.isfile(os.path.join(os.getcwd(), TOP_TWEET)):
        with open(os.path.join(os.getcwd(), TOP_TWEET), 'rb') as infile:
            in_dict = json.load(infile)
    else:
        in_dict = dict(id=None)
    return in_dict['id']


def _add_to_test_tweets(tweet_id, test_name):
    if os.path.isfile(os.path.join(os.getcwd(), TEST_TWEETS)):
        with open(os.path.join(os.getcwd(), TEST_TWEETS), 'rb') as infile:
            tweet_dict = json.load(infile)
    else:
        tweet_dict = {}

    tweet_dict[test_name] = tweet_id

    with open(os.path.join(os.getcwd(), TEST_TWEETS), 'wb') as outfile:
        json.dump(tweet_dict, outfile)


def _get_test_tweets():
    if os.path.isfile(os.path.join(os.getcwd(), TEST_TWEETS)):
        with open(os.path.join(os.getcwd(), TEST_TWEETS), 'rb') as infile:
            return json.load(infile).values()
    else:
        return dict()


class TestTwitter(unittest.TestCase):
    def test_get_timeline(self):
        t = Twitter(**twitter_access)
        user = twitter_username
        count = 6
        output = t.get_user_timeline(user=user, count=count)
        resp_user = set([i['user']['screen_name'] for i in output])

        # Set the ID for latest tweet before tests
        _write_top_tweet_file(output[0]['id'])

        self.assertEqual(1, len(resp_user))
        self.assertEqual(user, list(resp_user)[0])
        self.assertEqual(count, len(output))

    def test_post_only_text(self):
        t = Twitter(**twitter_access)
        tweet_text = "This is a test for plain text tweet at %r" % (_timenow())
        output = t.post_tweet(text=tweet_text)
        return_tweet_text = output.get('text')
        _add_to_test_tweets(output.get('id'), "text_only")
        self.assertEqual(tweet_text, return_tweet_text)

    def test_get_settings_geo_true(self):
        """
        This test should pass if user has turned the  account setting for Tweet location on using Twitter web/app
        :return:
        :rtype:
        """
        t = Twitter(**twitter_access)
        settings = t.get_account_settings()
        geo = settings.get('geo_enabled')

        self.assertEqual(True, geo)

    def test_post_with_latlong_geo_true(self):
        t = Twitter(**twitter_access)
        ll = (37.000880, -122.062309)
        tweet_text = "This is a test for plain text tweet with location at %r" % (_timenow())
        output = t.post_tweet(text=tweet_text, latlong=ll)
        return_tweet_text = output.get('text')
        _add_to_test_tweets(output.get('id'), "text_geo")

        self.assertEqual(tweet_text, return_tweet_text)
        if t.get_account_settings().get('geo_enabled'):
            return_ll = tuple(output['geo']['coordinates'])
            self.assertAlmostEqual(ll, return_ll)

    def test_post_with_media(self):
        t = Twitter(**twitter_access)
        tweet_text = "This is a test for tweet with 3 media at %r. Pictures from Pixabay." % (_timenow())
        jpegs = ['m01.jpg', 'm02.jpg', 'm03.jpg']
        media_list = [os.path.join('testing', i) for i in jpegs]
        output = t.post_tweet(text=tweet_text, media=media_list)
        return_tweet_text = output.get('text')
        _add_to_test_tweets(output.get('id'), "with_media")

        media_urls = [i['media_url_https'] for i in output['extended_entities']['media']]

        self.assertEqual(len(media_list), len(media_urls))

    @unittest.skipIf(_read_id_top_tweet() is None,
                     "Top ID not available before test. Delete test will not be performed")
    def test_delete_tweet(self):
        """
        Test deletion of tweets.
        Use the above tweets for deletion with the help of tweet_list
        :return:
        :rtype:
        """
        t = Twitter(**twitter_access)

        # Get current latest tweet ID
        latest_tweet = t.get_user_timeline(user=twitter_username, count=1)
        latest_tweet_id = latest_tweet[0].get('id')
        self.assertNotEqual(latest_tweet_id, _read_id_top_tweet())

        # Delete all test tweets
        for tweet_id in _get_test_tweets():
            output = t.delete_tweet(tweet_id=tweet_id)
            self.assertEqual(tweet_id, output.get('id'))

        # Get lates tweet ID after deletion
        latest_tweet = t.get_user_timeline(user=twitter_username, count=1)
        latest_tweet_id = latest_tweet[0].get('id')
        self.assertEqual(latest_tweet_id, _read_id_top_tweet())


if __name__ == "__main__":
    unittest.main()
