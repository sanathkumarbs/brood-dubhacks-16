#!flask/bin/python
from flask import Flask, jsonify
from Main import main
app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Get Tweets',
        'description': u'Get tweets of a user',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#@app.route('/TwitterApi/api/v1.0/tasks', methods=['GET'])
#@app.route('/TwitterApi/api/v1.0/GetTweets', methods=['GET'])
@app.route('/TwitterApi/api/v1.0/Tweets/<string:scr_name>', methods=['GET'])
def get_Tweets(scr_name):
    sucessful = False
    try:
        main(scr_name)
        sucessful = True
    except Exception as e:
        sucessful = False


    return jsonify({'successful': sucessful})

if __name__ == '__main__':
    app.run(debug=True)