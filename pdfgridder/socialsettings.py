import os


TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_REQUEST_TOKEN_URL = 'http://twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'http://twitter.com/oauth/access_token'
TWITTER_AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'

FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_API_KEY = os.environ['FACEBOOK_API_KEY']
FACEBOOK_API_SECRET = os.environ['FACEBOOK_API_SECRET']

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'users.social_auth.pipeline.ask_email',
    'users.social_auth.pipeline.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

GOOGLE_ANALYTICS_UA = os.environ['GOOGLE_ANALYTICS_UA']
