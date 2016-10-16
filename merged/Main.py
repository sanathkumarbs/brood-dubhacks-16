#!/usr/bin/env python
import sys
from AuthInfo import AuthInfo
from User import User
from Tweets import Tweets
from cognitive27 import Analyzer


class Main(object):

    def __init__(self):
        pass

    def CreateTweets(self,ScreenName):
        authinfo = AuthInfo()
        user = User(authinfo)
        tweets = Tweets()
        UserTweets = tweets.GetTweets(ScreenName,user)
        #FinalTweets = {}
        #FinalTweets[ScreenName] = UserTweets
        #print(UserTweets)
        return UserTweets




def main(ScreenName):
    #if __name__ == "__main__":
    The_main = Main()
    tweets = The_main.CreateTweets(ScreenName)
    newAnalyzer = Analyzer(ScreenName,tweets)
    newAnalyzer.Analyze()
    #print(tweets)

if len(sys.argv) > 1:
    screen_name = sys.argv[1]
else:
    screen_name = "@kayewest"#input("Please enter the screen name")
main(screen_name)
