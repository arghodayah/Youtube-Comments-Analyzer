import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import collections
from nltk.metrics.scores import f_measure
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
    #Check sentiment for a single element list
    if len(text)==1	:
        return classifier.classify(format_text(text[0]))
    #Check sentiment for multi-element list (video comments)
    elif len(text)>1:
        pos = 0
        neg = 0
        for item in text:
            if classifier.classify(format_text(item))=='positive':
                pos=pos+1
                print(str(pos+neg)+"/"+str(len(text)), end="\r")
            else:
                neg=neg+1
                print(str(pos+neg)+"/"+str(len(text)), end="\r")
        return pos, neg

def find_scores():
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
    #Split data into training(80%) and testing(20%) sets 
    training_set = pos[:int((.80)*len(pos))] + neg[:int((.80)*len(neg))]
    test_set = pos[int((.80)*len(pos)):] + neg[int((.80)*len(neg)):]
    #Training classifier    
    classifier = NaiveBayesClassifier.train(training_set)
    #Calculate scores	
    trueset = collections.defaultdict(set)
    testset = collections.defaultdict(set)
    #Test all test-set items using defined classifier
    for i, (text, label) in enumerate(test_set):
        trueset[label].add(i)
        result = classifier.classify(text)
        testset[result].add(i)
    return accuracy(classifier, test_set), f_measure(trueset['positive'], testset['positive']), f_measure(trueset['negative'], testset['negative'])
