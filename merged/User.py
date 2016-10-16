import tweepy
from AuthInfo import AuthInfo

class User(object):

    def __init__(self, AuthInfo):
        self.AuthInfo = AuthInfo

    def Authenticate(self):
        auth = tweepy.OAuthHandler(self.AuthInfo.consumer_key, self.AuthInfo.consumer_secret)
        auth.set_access_token(self.AuthInfo.access_token, self.AuthInfo.access_token_secret)
        api = tweepy.API(auth)
        return api