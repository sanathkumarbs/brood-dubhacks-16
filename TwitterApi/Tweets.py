import tweepy
from User import User
from AuthInfo import AuthInfo

class Tweets(object):

    def __init__(self):
        pass

    def GetTweets(self,screenName,user):
        api = user.Authenticate()
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screenName, count=100)
        #print("the first tweet")
        #print (new_tweets)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        #oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        #while len(new_tweets) > 0:
        counter = 0
        while counter > 0:
            #print("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screenName, count=2, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            counter -= 1
            #print("...%s tweets downloaded so far" % (len(alltweets)))

        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [ tweet.text.split('http')[0] for tweet in alltweets]
        """
        for x in outtweets:
            print("normal")
            print (x[0])
            print("printing utf 8")
            print(x[0].encode("utf-8"))
        #print(outtweets)
        """
        return outtweets

