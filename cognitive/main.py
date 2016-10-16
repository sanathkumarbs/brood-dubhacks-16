#!/usr/bin/env python
"""Summary.

Attributes:
    cachedStopWords (TYPE): Description
"""

import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
from nltk.corpus import stopwords
from firebase import firebase

cachedStopWords = stopwords.words("english")
cachedStopWords.append('RT')


class Cognitive(object):

    def __init__(self, body):
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body = body

    def get_keyphrases(self):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        try:
            conn = http.client.HTTPSConnection(
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
    """docstring for Fire"""

    def __init__(self, arg):
        super(Fire, self).__init__()
        self.arg = arg

    def get_users():
        firebase = firebase.FirebaseApplication(
            'https://brood-dubhacks-16.firebaseio.com/', None)


class Analyzer(object):

    def __init__(self, username, tweets):
        self.key = "2d81347e6bf6407abaf197986385cf1e"
        self.body_items = []
        self.tweets = tweets
        self.username = username

    def Analyze(self):
        body = self.build_body()
        print(body)
        cognitive = Cognitive(body)
        keyphrases = cognitive.get_keyphrases()
        keyphrases = ' '.join(keyphrases)
        print(keyphrases)

    def build_body(self):
        self.add_items_to_documents()
        body = json.dumps({
            "documents": self.body_items,
            "stopwords": cachedStopWords
        })
        return body

    def add_items_to_documents(self):
        for idee in range(len(self.tweets) - 2):
            docIdee = {
                "language": "en",
                "id": idee,
                "text": self.tweets[idee]}
            self.body_items.append(docIdee)

        idee = len(self.tweets) - 1

        docIdee = {
            "language": "en",
            "id": idee,
            "text": self.tweets[idee]}
        self.body_items.append(docIdee)

if __name__ == "__main__":

    tweets = ["650+ hackers all set to hack all night!  Tonight's gonna be a good night ;-) #dubhacks16 @DubHacks @MLHacks",
              "@vidsrinivasan How to integrate inclusive design into ideation. Our DubHacks keynote speaker, Vidya Srinivasan.",
              "So true! Thanks for the great keynote @vidsrinivasan!",
              "These are not hotwheels. Ballers from my hometown doing their thing!"]

    analyzer = Analyzer('SanathKumarBS', tweets)
    analyzer.build_body()

    # print(body)

    # cognitive = Cognitive(body)
    # keyphrases = cognitive.get_keyphrases()
    # keyphrases = ' '.join(keyphrases)
    # print(keyphrases)
