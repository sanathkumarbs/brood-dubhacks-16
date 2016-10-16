#!/usr/bin/env python
"""Summary.

Attributes:
    cachedStopWords (TYPE): Description
"""

import httplib
import urllib
import base64
import json
from nltk.corpus import stopwords
from firebase import firebase

cachedStopWords = stopwords.words("english")
cachedStopWords.append('RT')


class Cognitive(object):
    """Summary

    Attributes:
        body (TYPE): Description
        key (str): Description
    """

    def __init__(self, body):
        """Summary

        Args:
            body (TYPE): Description
        """
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body = body

    def get_keyphrases(self):
        """Summary

        Returns:
            TYPE: Description
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
    """docstring for Fire

    Attributes:
        firebase (TYPE): Description
        username (TYPE): Description
    """

    def __init__(self, username):
        """Summary

        Args:
            username (TYPE): Description
        """
        self.username = username
        self.firebase = firebase.FirebaseApplication(
            'https://brood-dubhacks-16.firebaseio.com/', None)

    def get_userid(self):
        """Summary

        Returns:
            TYPE: Description
        """
        print("/twitter/" + self.username)
        result = self.firebase.get('/twitter/' + self.username, None)
        return result

    def get_tags(self, user):
        """Summary

        Args:
            user (TYPE): Description

        Returns:
            TYPE: Description
        """
        result = self.firebase.get("/tags/" + user + "/", None)
        for key in result.keys():
            tag = tag = result[key]
        return tag

    def post_tags(self, user, tag):
        """Summary

        Args:
            user (TYPE): Description
            tag (TYPE): Description

        Returns:
            TYPE: Description
        """
        result = self.firebase.post("/tags/" + user + "/", tag)
        return result


class Analyzer(object):
    """Summary

    Attributes:
        body_items (list): Description
        key (str): Description
        tweets (TYPE): Description
        username (TYPE): Description
    """

    def __init__(self, username, tweets):
        """Summary

        Args:
            username (TYPE): Description
            tweets (TYPE): Description
        """
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body_items = []
        self.tweets = tweets
        self.username = username

    def Analyze(self):
        """Summary

        Returns:
            TYPE: Description
        """
        body = self.build_body()

        cognitive = Cognitive(body)
        keyphrases = cognitive.get_keyphrases()
        keyphrases = ' '.join(keyphrases)
        print(keyphrases)

        self.update_firebase(keyphrases)

    def exec_recommender():
        """Summary

        Returns:
            TYPE: Description
        """
        call_me(self.username)

    def update_firebase(self, tags):
        """Summary

        Args:
            tags (TYPE): Description

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
        """Summary

        Returns:
            TYPE: Description
        """
        self.add_items_to_documents()
        body = json.dumps({
            "documents": self.body_items,
            "stopwords": cachedStopWords
        })
        return body

    def add_items_to_documents(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if(len(self.tweets) > 1):
            # print (self.tweets)
            for idee in range(len(self.tweets)):
                if(len(self.tweets[idee]) > 0):
                    docIdee = {
                        "language": "en",
                        "id": idee,
                        "text": self.tweets[idee]}
                    self.body_items.append(docIdee)

if __name__ == "__main__":
    tweets = ["650+ hackers all set to hack all night!  Tonight's gonna be a good night ;-) #dubhacks16 @DubHacks @MLHacks",
              "@vidsrinivasan How to integrate inclusive design into ideation. Our DubHacks keynote speaker, Vidya Srinivasan.",
              "So true! Thanks for the great keynote @vidsrinivasan!",
              "These are not hotwheels. Ballers from my hometown doing their thing!"
              ]

    analyzer = Analyzer('SanathKumarBS', tweets)
    analyzer.Analyze()

    # print(body)

    # cognitive = Cognitive(body)
    # keyphrases = cognitive.get_keyphrases()
    # keyphrases = ' '.join(keyphrases)
    # print(keyphrases)
