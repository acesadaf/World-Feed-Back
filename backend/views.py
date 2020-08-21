from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import tweepy
import requests
import json
import reverse_geocoder as rg
from django.http import JsonResponse
from backend.models import CountryTweetCache, CityTweetCache
consumer_key = "I7VpkNuclA6KETbxU1fj2IIav"
consumer_secret = "9GoP6ZEbBRpCEPyBZ4GiWomgvDwBjGnat0iwIJBexMRVvq2pHm"
access_token = "1007201002930335744-kbdzzTCMrjRZIGq155Teu2MBASozOb"
access_token_secret = "myKU6wuYz3ync8aSTfbpD3hvR0I51OjCAB4aI4qyiRHV9"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

news_api_key = "c3677ea6a98b4e13a34afccee2199218"

# Create your views here.


def cache_city(city, country, tweets):
    ctc = CityTweetCache(city=city, country=country, tweets=tweets)
    ctc.save()


def fetch_city_cache(city, country):
    tweets = []
    cached_tweets = CityTweetCache.objects.get(
        city=city, country=country)
    print("fetching from city cache!")
    for tweet in cached_tweets.tweets:
        split_tweet = tweet.split("|||")
        tweets.append({
            'username': split_tweet[0],
            'tweet': split_tweet[1],
            'url': split_tweet[2]
        })

    return tweets


def fetch_country_cache(country):
    tweets = []
    cached_tweets = CountryTweetCache.objects.get(country=country)
    print("fetching from country cache!")
    for tweet in cached_tweets.tweets:
        split_tweet = tweet.split("|||")
        tweets.append({
            'username': split_tweet[0],
            'tweet': split_tweet[1],
            'url': split_tweet[2]
        })
    return tweets


def cache_country(country, tweets):
    ctc = CountryTweetCache(country=country, tweets=tweets)
    ctc.save()


def prepare_tweets(place_id):
    print("API call!")
    tweets, to_cache = api_call(place_id=place_id, popular=True, tweet_count=5)
    if len(tweets) < 5:
        remaining_tweets, remaining_cache = api_call(
            place_id=place_id, popular=False, tweet_count=5 - len(tweets))

        tweets.extend(remaining_tweets)
        to_cache.extend(remaining_cache)

    return tweets, to_cache


def api_call(place_id, popular, tweet_count):
    tweets = []
    to_cache = []
    if popular:
        call = tweepy.Cursor(api.search, result_type="popular",
                             q="place:{} -filter:retweets".format(place_id)).items(tweet_count)
    else:
        call = tweepy.Cursor(
            api.search, q="place:{} -filter:retweets".format(place_id)).items(tweet_count)
    for tweet in call:
        u, t, url = tweet.user.screen_name, tweet._json['text'], "https://twitter.com/{}/status/{}".format(
            tweet.user.screen_name, tweet.id)
        tweets.append({'username': u,
                       'tweet': t, 'url': url})
        tweet_to_cache = "{}|||{}|||{}".format(
            u, t, url)
        to_cache.append(tweet_to_cache)

    return tweets, to_cache


def api_fetch_and_cache(body, city, country, granularity):
    # using Twitter geocoder here, necessary to get place_id for the twitter call
    try:
        places = api.reverse_geocode(
            lat=body['lat'], long=body['lng'], granularity=granularity)
        place_id = places[0].id

        tweets, to_cache = prepare_tweets(place_id)
        if granularity == "country":
            cache_country(country, to_cache)

        else:
            cache_city(city, country, to_cache)

    except:
        tweets = [{'username': "World Feed",
                   'tweet': "Sorry, No tweets from here :(", 'url': "http://localhost:3000/"}]

    return tweets


@csrf_exempt
def get_tweet(request):
    body = json.loads(request.body)
    tweets = []
    # using an offline reverse geocoder here to minimize API calls
    coordinates = (float(body['lat']), float(body['lng']))
    location_names = rg.search(coordinates)
    city, country = location_names[0]['admin1'], location_names[0]['cc']
    typ = body["type"]
    print(city, country)

    if typ == "country":
        if CountryTweetCache.objects.filter(country=country).exists():
            tweets = fetch_country_cache(country)

        else:
            tweets = api_fetch_and_cache(body, city, country, "country")

    else:
        if CityTweetCache.objects.filter(city=city, country=country).exists():
            tweets = fetch_city_cache(city=city, country=country)

        else:
            tweets = api_fetch_and_cache(body, city, country, "city")

    return JsonResponse(tweets, safe=False)


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

    # r = requests.get(videos_url, params=params, verify=False)
    result = r.json()
    links = []
    for video in result['items']:
        links.append(videos_url + video['id']['videoId'])

    # print(r.json())
    print(links)
    return HttpResponse("OK")
