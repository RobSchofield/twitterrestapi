#!/usr/bin/env python
'''
Downloads all of the followers and their bios and tweets a given page.
'''
import pickle
import twitterrestapi


def pickle_data(bios, tweets, file_part):
    '''
    Pickle the bios and tweets and return empty list.
    '''
    print(bios)
    with open('bios_' + str(file_part) + '.pkl', 'wb') as f:
        pickle.dump(bios, f)
        bios = []
    with open('tweets_' + str(file_part) + '.pkl', 'wb') as f:
        pickle.dump(tweets, f)
        tweets = []
    return bios, tweets


def download(followers, max_followers, save_length):
    '''
    Download the followers and save the bio and tweets in
    chunks of save_length.
    '''
    file_part = 0
    tweets = []
    bios = []
    if max_followers < len(followers):
        followers = followers[:max_followers]
    for _, follower in enumerate(followers):
        try:
            tweets.append(tam.get_tweets(follower))
        except:
            print('No tweets')
            tweets.append([])
        try:
            bios.append(tam.get_bio(follower))
        except:
            print('No bio')
            bios.append([])
        print(_)
        if (_ + 1) % save_length == 0:
            bios, tweets = pickle_data(bios, tweets, file_part)
            file_part += 1
    return None


def import_followers_ids(file_name):
    '''
    Imports follower's ids from a text file.
    '''
    followers_ids = []
    with open(file_name, 'r') as f:
        followers_ids = f.read().split('\n')
    return followers_ids

if __name__ == '__main__':
    tam = twitterrestapi.TwitterAdManager('', '', '', '')

    #followers = import_followers_ids()
    followers = tam.get_following()

    save_length = 10
    max_followers = 20
    download(followers, max_followers, save_length)


