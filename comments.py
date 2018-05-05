from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#API parameters
DEVELOPER_KEY = "AIzaSyBh9Gejah1BDmM3BsemT9wt3lHSBz9vsA8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def get_comments(videoID):
    try:
        comments = []
        #Execute API request
        response = youtube.commentThreads().list(part="snippet",videoId=videoID,textFormat="plainText",maxResults=100).execute()
        #Extract comments text from API response
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]
            comment_text = comment["snippet"]["textDisplay"]
            comments.append(comment_text)
        try:
            nextToken = response["nextPageToken"]
        except:
	        nextToken = None
        #Get next page of comments
        while nextToken is not None:
            response = youtube.commentThreads().list(part="snippet",videoId=videoID,textFormat="plainText",pageToken=response["nextPageToken"],maxResults=100).execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]
                comment_text = comment["snippet"]["textDisplay"]
                comments.append(comment_text)
            try:
                nextToken = response["nextPageToken"]
            except:
	            nextToken = None
        return comments
    except:
        return "Error"