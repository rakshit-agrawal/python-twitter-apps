"""
Information about Twitter Public API.

-Rakshit Agrawal, 2016


Last updated: May 11, 2016
"""

# URLs for specific API endpoints
URL = {
    'user_timeline': "https://api.twitter.com/1.1/statuses/user_timeline.json",
    'search': "https://api.twitter.com/1.1/search/tweets.json",
    'post_tweet': "https://api.twitter.com/1.1/statuses/update.json",
    'media_upload': "https://upload.twitter.com/1.1/media/upload.json",
    'account_settings': "https://api.twitter.com/1.1/account/settings.json",
    'destroy_tweet':"https://api.twitter.com/1.1/statuses/destroy/%r.json"
}