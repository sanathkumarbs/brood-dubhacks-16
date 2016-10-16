import sys
from AuthInfo import AuthInfo
from User import User
from Tweets import Tweets

class Main(object):

    def __init__(self):
        pass

    def CreateTweets(self,ScreenName):
        authinfo = AuthInfo()
        user = User(authinfo)
        tweets = Tweets()
        UserTweets = tweets.GetTweets(ScreenName,user)
        FinalTweets = {}
        FinalTweets[ScreenName] = UserTweets
        return FinalTweets




def main(ScreenName):
    #if __name__ == "__main__":
    The_main = Main()
    tweets = The_main.CreateTweets(ScreenName)
    print(tweets)

if len(sys.argv) > 1:
    screen_name = sys.argv[1]
else:
    screen_name = "@sanathkumarbs"#input("Please enter the screen name")
main(screen_name)