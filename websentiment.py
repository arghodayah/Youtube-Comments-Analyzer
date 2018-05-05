from flask import Flask
from flask import request
from flask import Response
from flask import json
import nltk
nltk.download('stopwords')
from nltk.classify import NaiveBayesClassifier

app = Flask(__name__)
#Root response
@app.route("/")
def websentiment():
    #Get text argument from URL
    text = request.args.get('text')
    #Find sentiment and return in JSON style
    data = {
        'Text'  : text,
        'Sentiment' : find_sentiment(text)
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp
	
def find_sentiment(text):
    #Text formatting to classify
    def format_text(text):
        return({word: True for word in nltk.word_tokenize(text)})
    #Load positive categorized text
    pos = []
    with open("./pos.txt", encoding='ISO-8859-1') as f:
        for i in f:
            pos.append([format_text(i), 'positive'])
    #Load negative categorized text
    neg = []
    with open("./neg.txt", encoding='ISO-8859-1') as f:
        for i in f:
            neg.append([format_text(i), 'negative'])
    #Training classifier
    training_set = pos + neg
    classifier = NaiveBayesClassifier.train(training_set)
	
    return classifier.classify(format_text(text))
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')