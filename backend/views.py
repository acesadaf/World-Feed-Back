from django.shortcuts import render
from django.http import HttpResponse
import tweepy
import requests

consumer_key = "I7VpkNuclA6KETbxU1fj2IIav"
consumer_secret = "9GoP6ZEbBRpCEPyBZ4GiWomgvDwBjGnat0iwIJBexMRVvq2pHm"
access_token = "1007201002930335744-kbdzzTCMrjRZIGq155Teu2MBASozOb"
access_token_secret = "myKU6wuYz3ync8aSTfbpD3hvR0I51OjCAB4aI4qyiRHV9"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

news_api_key = "c3677ea6a98b4e13a34afccee2199218"


# Create your views here.


def get_tweet(request):
    tweets = []
    for tweet in tweepy.Cursor(api.search, q="#" + "tweeting" + " -filter:retweets", rpp=5, lang="en", tweet_mode="extended").items(1):
        print(tweet)

    return HttpResponse("OK")


def get_news(request):
    url = ('http://newsapi.org/v2/top-headlines?'
           'sources=bbc-news&'
           'apiKey={}'.format(news_api_key))

    response = requests.get(url)
    print(response.json())
    return HttpResponse("OK")


def get_videos(request):
    search_url = "https://www.googleapis.com/youtube/v3/search"

    videos_url = "https://www.youtube.com/watch?v="

    params = {
        'part': 'snippet',
        'q': 'bangladesh',
        'key': 'AIzaSyDwvNf66Sbjxr8Iou7Z2kEqyNbEFkNTCqU'}

    r = requests.get(search_url, params=params, verify=False)

    #r = requests.get(videos_url, params=params, verify=False)
    result = r.json()
    links = []
    for video in result['items']:
        links.append(videos_url + video['id']['videoId'])

    # print(r.json())
    print(links)
    return HttpResponse("OK")
