import httplib2
import os
import sys
import pymongo
from pymongo import MongoClient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from comments import get_comments
from topics import find_topics
from sentiment import find_sentiment
from sentiment import find_scores

#Read arguments
try:
    tool  = None
    first_arg = None
    second_arg = None
    tool = sys.argv[1]
    first_arg = sys.argv[2]
    second_arg = sys.argv[3]
except:
    pass
		
def topics(quantity, videos):
    videos_list = []
    all_comments = []
    found_topics = []
    #Check if single or multi-video request
    if ',' in videos:
        videos_list = videos.split(",")
    else:
        videos_list.append(videos)	
    #Get comments and save to db
    for video in videos_list:
        print("- Collecting comments of " + video + " video...")
        if get_comments(video) == "Error":
            print("Error")
        else:
            comments = []
            comments.extend(get_comments(video))
            #Add comments to db
            connection = MongoClient('localhost',27017)
            yt_db = connection.yt
            comments_coll = yt_db.comments
            person = [{'video':video, 'comment':comment} for comment in comments]
            comments_coll.insert(person)
            connection.close()
            print(str(len(comments)) + " comments found and added to db")
            all_comments.extend(comments)
    #Get top quantity topics
    print("- Finding topics out of " + str(len(all_comments)) + " comments...")			
    found_topics.extend(find_topics(all_comments, quantity)) if len(all_comments)>0 else print("No comments to analyze")
    for topic in found_topics:
        print("Topic: %s" % (topic,))

def sentiment(type, input):
    if type == 'video':
        pos = 0
        neg = 0
        #Get comments and save to db
        print("- Collecting comments of " + input + " video...")
        if get_comments(input) == "Error":
            print("Error")
        else:
            comments = []
            comments.extend(get_comments(input))
            #Add comments to db
            connection = MongoClient('localhost',27017)
            yt_db = connection.yt
            comments_coll = yt_db.comments
            person = [{'video':input, 'comment':comment} for comment in comments]
            comments_coll.insert(person)
            connection.close()
            print(str(len(comments)) + " comments found and added to db")
            #Get comments' sentiment summary
            print("- Finding sentiment...")			
            if len(comments)>0:
                results = find_sentiment(comments)
                print(str(len(comments)) + " comments were analyzed.")
                print("Positive comments: " + str(results[0]) + " = " + str(round((results[0]/len(comments))*100, 2)) + "%")
                print("Negative comments: " + str(results[1]) + " = " + str(round((results[1]/len(comments))*100, 2)) + "%")
            else:
                print("No comments to analyze")
    elif type == 'text':
        #Get sentiment of submitted text
        text = []
        text.append(input)
        print("Sentiment: " + find_sentiment(text))	
		
def initial(tool=tool, arg1=first_arg, arg2=second_arg):
    #Check requested tool
    if(tool=='topics' and arg1 is not None and arg2 is not None):
	    topics(arg1, arg2)
    elif(tool=='sentiment' and arg1 is not None and arg2 is not None):
	    sentiment(arg1, arg2)
    elif(tool=='sentiment' and arg1=='scores' and arg2 is None):
        #Get sentiment analyzer scores
        scores = []
        scores.extend(find_scores())
        print("Accuracy: " + str(round(scores[0]*100, 2)) + "%")
        print("F1 Score (Pos): " + str(round(scores[1]*100, 2)) + "%")
        print("F1 Score (Neg): " + str(round(scores[2]*100, 2)) + "%")
    else:
        #Script usage description
        print("Usage: analyze.py Tool Arg1 Arg2")
        print("Tool: 'topics' or 'sentiment'")
        print("Arg1: topics=>Quantity of topics, sentiment=>'video' or 'text'")
        print("Arg2: topics=>Videos IDs seperated by commas(,), sentiment=>Video ID or Text")

if __name__ == "__main__":
    initial()