import base64
import json
from pprint import pprint
import oauth2 as oauth

import requests
from requests_oauthlib import OAuth1
from credentials import CONSUMER_KEY, CONSUMER_SECRET
from credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET

URL = {
    'access_token':"https://api.twitter.com/oauth2/token",
    'user_timeline':"https://api.twitter.com/1.1/statuses/user_timeline.json",
    'search':"https://api.twitter.com/1.1/search/tweets.json",
    'post_tweet':"https://api.twitter.com/1.1/statuses/update.json",
    'account_settings':"https://api.twitter.com/1.1/account/settings.json",
    'media_upload':"https://upload.twitter.com/1.1/media/upload.json",
    'post_tweet_with_media':""

}



def _get_headers(token, type):
    if type=="basic":
        auth_token = type.title() + " " + base64.b64encode(token)
    else:
        auth_token = type.title() + " " + token

    headers = {
        'Authorization':auth_token,
        'Content-Type':"application/x-www-form-urlencoded;charset=UTF-8"
    }

    return headers

def _get_access_token(url, CONSUMER_KEY, CONSUMER_SECRET):

    values = {'grant_type': "client_credentials"}
    raw_token = CONSUMER_KEY + ":" + CONSUMER_SECRET
    headers = _get_headers(raw_token, type="basic")

    token = requests.post(url, data=values, headers=headers)
    token = token.json()
    token_type = token["token_type"]
    access_token = token["access_token"]

    return access_token, token_type


def _access_headers(extra_headers={}):

    access_token, token_type = _get_access_token(url=URL["access_token"],
                                                 CONSUMER_KEY=CONSUMER_KEY,
                                                 CONSUMER_SECRET=CONSUMER_SECRET)
    headers = _get_headers(access_token, token_type)
    headers.update(extra_headers)

    pprint(headers)
    return headers


def get_data(type, values, extra_headers={}):

    access_token, token_type = _get_access_token(url=URL["access_token"],
                                                 CONSUMER_KEY=CONSUMER_KEY,
                                                 CONSUMER_SECRET=CONSUMER_SECRET)
    url = URL[type]

    headers = _get_headers(access_token, token_type)
    headers.update(extra_headers)

    result = requests.get(url=url, headers=headers, params=values)

    return result


def user_tweets():
    screen_name = "crowd_policy"
    result = get_data(type="user_timeline", values = dict(screen_name=screen_name,count=20))#{'screen_name':screen_name, 'count':20})

    result = result.json()
    print type(result)
    new_result = [x['text'] for x in result]
    return dict(result=new_result)


def post_new_tweet(status="TestStatus"):
    """

    :return:
    :rtype:
    """
    params = dict(status=status)
    url = URL['post_tweet']

    # resp = requests.post(url=url, data=data, headers=_access_headers())

    # Set up instances of our Token and Consumer. The Consumer.key and
    # Consumer.secret are given to you by the API provider. The Token.key and
    # Token.secret is given to you after a three-legged authentication.
    token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)

    # Set our token/key parameters
    params['oauth_token'] = token.key
    params['oauth_consumer_key'] = consumer.key

    # Create our request. Change method, etc. accordingly.
    req = oauth.Request(method="POST", url=url, parameters=params)

    # Sign the request.
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)
    print req

def get_account_settings():
    url = URL['account_settings']
    resp = requests.get(url=url, headers=_access_headers())

    print resp.json()



def post_tweet(status = "test tweet"):
    url = URL['post_tweet']
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    twt = requests.post(url=url, auth=auth, params=dict(status=status))

    print twt.json()


def post_tweet_with_media(status, media):

    url = URL['post_tweet']
    media_url = URL['media_upload']
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    with open(media,'rb') as mediafile:
        media = requests.post(url=media_url, files=dict(media=mediafile), auth=auth)

    print media.json()
    media_id = media.json().get('media_id')

    twt = requests.post(url=url, auth=auth, params=dict(status=status, media_ids=media_id))

    print twt.json()


if __name__=="__main__":

    status = "Hi this is a tweet using API for test without media"
    media = 'media01.gif'
    # post_new_tweet(status=status)
    # get_account_settings()

    post_tweet(status)
    # post_tweet_with_media(status, media)