from fastapi import APIRouter
from search_app import search
import sys
import os

# creating the router object
router = APIRouter()
# setting the working directory
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURR_DIR)

@router.post("/searchapp/")
def searchapp(username_user_info = None, user_id_for_tweets = None, username_tweets = None, user_id_get_screen_name = None, tweet_id = None, keyword = None, hashtags = None, location = None, time_range = None, sort_criterion = 'popularity', distance = 100000, top10users = 'no', trendingTweets = 'no', limit = 10):
    output = search(username_user_info, user_id_for_tweets, username_tweets, user_id_get_screen_name, tweet_id, keyword, hashtags, location, time_range, sort_criterion, distance, top10users, trendingTweets, limit)
    return output
