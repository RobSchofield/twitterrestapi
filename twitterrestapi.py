#!/usr/bin/env python
'''
This library can retrieve data from Twitters Rest API.

Current functions:
    request_rest
    get_tweets
    get_bio
    get_followed
    get_following
    search_for_keywords
'''

import json
import time
import urllib.request
import urllib.error
import oauth2 as oauth


twitter_base_rest = 'https://api.twitter.com/1.1/'

class TwitterRestAPI(object):

    def __init__(self, consumer_key='', consumer_secret='', access_token='', access_token_secret=''):
        '''
        Initialize the session.
        '''
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = oauth.Token(key=access_token, secret=access_token_secret)
        self.access_token_secret = access_token_secret
        self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        self.client = oauth.Client(self.consumer, self.access_token)
        self.accounts = None

    def request_rest(self, request, request_type='GET', print_response=False):
        '''
        Request data from the twitter rest API.
        '''
        r_url = '%s%s' % (twitter_base_rest,
                          request)
        resp, content = self.client.request(r_url, request_type)
        parsed_json = json.loads(content.decode('utf-8'))
        if print_response:
            print(resp)
        return parsed_json

    def get_tweets(self, user_id):
        '''
        Retrieves the tweets of a given user_id.
        '''
        count = 200
        tweets = []
        request = 'statuses/user_timeline.json?user_id=%s&count=200' % (user_id)
        while count > 199:
            ids = []
            data = self.request_rest(request)
            for tweet in data:
                tweets.append(tweet['text'])
                ids.append(tweet['id'])
            max_id = sorted(ids)[0]
            request = 'statuses/user_timeline.json?user_id=%s&count=200&max_id=%s' % (user_id, max_id)
            data = self.request_rest(request)
            count = len(data)
            time.sleep(1)
        return tweets

    def get_bio(self, user_id):
        '''
        Retrieves the bio of a given user_id.
        '''
        request = 'users/show.json?user_id=%s&include_entities=false' % (user_id)
        time.sleep(1)
        return [self.request_rest(request)['description']]

    def get_followed(self, screen_name):
        '''
        Retrives a list of followed a user's screen name.
        '''
        cursor = -1
        followed = []
        while cursor != 0:
            request = 'friends/list.json?cursor=%d&screen_name=%s&count=200&skip_status=true&include_user_entities=false' % (cursor, screen_name)
            data = self.request_rest(request)
            cursor = data['next_cursor']
            for user in data['users']:
                if user['lang'] == 'en':
                    followed.append(user['screen_name'])
        return followed

    def get_following(self, screen_name):
        '''
        Retrives a list of followers by a user's screen name.
        '''
        cursor = -1
        following = []
        with open(screen_name + '_followers.txt', 'a') as f:
            while cursor != 0:
                request = 'followers/ids.json?cursor=%d&screen_name=%s&count=5000' % (cursor, screen_name)
                data = self.request_rest(request)
                cursor = data['next_cursor']
                for user in data['ids']:
                    following.append(str(user))
                    f.write(str(user) + '\n')
                    f.flush()
                time.sleep(70)
        return following

    def search_for_keywords(self, keyword, max_id='0'):
        '''
        Searches tweets for a keyword.
        '''
        tweets = []
        request = 'search/tweets.json?q=%%23%s&count=100&since_id=%s' % (keyword, max_id)
        for tweet in self.request_rest(request)['statuses']:
            if max_id is None:
                max_id = tweet['id']
            tweets.append(tweet['text'])
        return tweets, max_id

if __name__ == '__main__':
    print('twitterrestapi.py')
