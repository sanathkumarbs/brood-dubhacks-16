#!/usr/bin/env python
"""Summary.

Attributes:
    cachedStopWords (list): caching StopWords from nltk library for cleaning
"""

import httplib
import urllib
import base64
import json
from nltk.corpus import stopwords
from firebase import firebase
from brood import call_me

cachedStopWords = stopwords.words("english")
cachedStopWords.append('RT')


class Cognitive(object):
    """Methods related to Microsoft Cognitive Services - Text Analytics API.

    Attributes:
        body (TYPE): http request body
        key (str): key
    """

    def __init__(self, body):
        """Initialization.

        Args:
            body (TYPE): http request body
        """
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body = body

    def get_keyphrases(self):
        """Getting all tags.

        Returns:
            Returns all tags
        """
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        try:
            conn = httplib.HTTPSConnection(
                'westus.api.cognitive.microsoft.com')
            conn.request("POST", "/text/analytics/v2.0/keyPhrases",
                         self.body, headers)
            response = conn.getresponse()
            data = response.read()
            # print(data)
            jsondata = json.loads(data.decode('utf-8'))
            keyphrases = []
            for element in jsondata['documents']:
                # print (element['keyPhrases'])
                keyphrases += element['keyPhrases']
            # print(jsondata['documents'][0]['keyPhrases'])
            return keyphrases
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


class Fire(object):
    """Methods for Firebase.

    Attributes:
        firebase: Instance of the firebase object
        username: Twitter Username to be analyzed
    """

    def __init__(self, username):
        """Initialization.

        Args:
            username (string): Twitter Username to be analyzed
        """
        self.username = username
        self.firebase = firebase.FirebaseApplication(
            'https://brood-dubhacks-16.firebaseio.com/', None)

    def get_userid(self):
        """Get userid for the given Twitter Handle.

        Returns:
            result: firebase json result
        """
        print("/twitter/" + self.username)
        result = self.firebase.get('/twitter/' + self.username, None)
        return result

    def get_tags(self, user):
        """Get tags analyzed for the given Twitter handle/user.

        Args:
            user (TYPE): Description

        Returns:
            result: firebase json result
        """
        result = self.firebase.get("/tags/" + user + "/", None)
        for key in result.keys():
            tag = tag = result[key]
        return tag

    def post_tags(self, user, tag):
        """Post tags of an user to Firebase.

        Args:
            user (str): Twitter Username
            tag (str): Analyzed Tags for user

        Returns:
            result: firebase json result
        """
        result = self.firebase.post("/tags/" + user + "/", tag)
        return result


class Analyzer(object):
    """Analyzing Engine for Tweets.

    Attributes:
        body_items (list): Description
        key (str): Description
        tweets (TYPE): Description
        username (TYPE): Description
    """

    def __init__(self, username, tweets):
        """Initialization.

        Args:
            username (str): Twitter Username
            tweets (str): Tweets Analyzed
        """
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body_items = []
        self.tweets = tweets
        self.username = username

    def Analyze(self):
        """Analyzing Tweets.

        Returns:
            TYPE: Description
        """
        body = self.build_body()

        cognitive = Cognitive(body)
        keyphrases = cognitive.get_keyphrases()
        keyphrases = ' '.join(keyphrases)
        print(keyphrases)

        self.update_firebase(keyphrases)

    def exec_recommender(self):
        """Execute Recommender Engine.

        Returns:
            TYPE: Description
        """
        call_me(self.username)

    def update_firebase(self, tags):
        """Update Firebase with new analysis.

        Args:
            tags (string): string

        Returns:
            TYPE: Description
        """
        fire = Fire(self.username)
        userid = fire.get_userid()
        print(userid)

        result = fire.post_tags(userid, tags)
        print(result)

        print("Checking tags")
        print(fire.get_tags(userid))

    def build_body(self):
        """Building body for http request.

        Returns:
            body: Body for the http request
        """
        self.add_items_to_documents()
        body = json.dumps({
            "documents": self.body_items,
            "stopwords": cachedStopWords
        })
        return body

    def add_items_to_documents(self):
        """Adding items to the documents of the body.

        Returns:
            body_items: Each unique document is created per tweet
        """
        if(len(self.tweets) > 1):
            # print (self.tweets)
            for idee in range(len(self.tweets)):
                if(len(self.tweets[idee]) > 0):
                    docidee = {
                        "language": "en",
                        "id": idee,
                        "text": self.tweets[idee]}
                    self.body_items.append(docidee)

if __name__ == "__main__":
    tweets = ["650+ hackers all set to hack all night! Tonight's",
              "gonna be a good night ;-) #dubhacks16 @DubHacks @MLHacks",
              "@vidsrinivasan How to integrate inclusive design into ideation"
              "Our DubHacks keynote speaker, Vidya Srinivasan.",
              "So true! Thanks for the great keynote @vidsrinivasan!",
              "These aren't hotwheels. Ballers from my town doing their thing!"
              ]

    analyzer = Analyzer('SanathKumarBS', tweets)
    analyzer.Analyze()

    # print(body)

    # cognitive = Cognitive(body)
    # keyphrases = cognitive.get_keyphrases()
    # keyphrases = ' '.join(keyphrases)
    # print(keyphrases)
