# The folowing code is used to help search tweets with keyword

# The following codes for connecting to Twitter API to get full conversation are adapted from the sample codes given by Twitterdev through GitHub repository: https://github.com/twitterdev/Twitter-API-v2-sample-code/tree/main/Recent-Search

import requests
import os
import json
import pandas as pd
import numpy as np
import dateutil.parser

# Run the belowing commented code the first time
os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAEhJSAEAAAAAw90%2FVLZI6GYFEZRGU%2BOvBN9BPDI%3Dw8vYd8VSnbAkgKMkmwnUKng7zSgCM7xdYLJkUx3N62eReol8hs'

bearer_token = os.environ.get("TOKEN")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def create_url(keyword, max_results):  # If you are retrieving recent tweets, remove "start_date" and "end_date"

    search_url = "https://api.twitter.com/2/tweets/search/recent"  # collect recent tweets (last 7 days)

    # For understanding of the fields available, please check: https://developer.twitter.com/en/docs/twitter-api/fields
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings',
                    # Note:"source" field has been removed
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, params, next_token=None):
    params['next_token'] = next_token  # params object received from create_url function
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# you don't need to define the time, if you only can search for recent tweets
max_results = 10  # you can set 10-500
keyword = 'specialty coffee'
# here is the official documentation to help you understand how to build query with correct operators: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

# Remember with standard account, you can only retrieve recent 7-day tweets with search_tweet endpoint, so when you are setting the timeframe the earliest date you can set is 7 day before your current date
url = create_url(keyword, max_results)
json_response = connect_to_endpoint(url[0], url[1])

# print(json.dumps(json_response, indent=4, sort_keys=True))

# you can check the tweets field and user field and get any field you want by modifying the following list
user_id =[]
username=[]
user_followers =[]
user_verified =[]
user_description=[]
tweet_id =[]
created_at =[]
retweet_count = []
reply_count = []
like_count = []
quote_count = []

for tweet in json_response['data']:
    user_id.append(tweet['author_id'])
    tweet_id.append(tweet['id'])
    created_at.append(dateutil.parser.parse(tweet['created_at']))
    retweet_count.append(tweet['public_metrics']['retweet_count'])
    reply_count.append(tweet['public_metrics']['reply_count'])
    like_count.append(tweet['public_metrics']['like_count'])
    quote_count.append(tweet['public_metrics']['quote_count'])

for user in json_response['includes']['users']:
    username.append(user['username'])
    user_followers.append(user['public_metrics']['followers_count'])
    user_verified.append(user['verified'])
    user_description.append(user['description'])

df = pd.DataFrame(list(zip(user_id, username, user_followers, user_verified, user_description, tweet_id, created_at,
                           retweet_count, reply_count, like_count, quote_count)),
                  columns=['user_id', 'username', 'user_followers','user_verified', 'user_description',
                           'tweet_id', 'created_at','retweet_count','reply_count', 'like_count', 'quote_count'])

df.to_csv('tweet.csv', index=False)
