import tweepy
from textblob import TextBlob
import googlemaps


def find_nearest_mall(latitude, longitude, api_key):
    gmaps = googlemaps.Client(key=api_key)
    places_result = gmaps.places_nearby(location=(latitude, longitude), radius=5000, type='shopping_mall')
    if places_result['results']:
        return places_result['results'][0]['name']
    else:
        return None


def analyze_sentiment(keyword, num_tweets):
    consumer_key = '0kAvfJq5noqFIBjkcI8ls7fMe'
    consumer_secret = 'RO8R1mP8zOMVausBadyfUtkcRyopo5kwrTl2QRrCscIwazyvhB'
    access_token = '1267184729536815104-sIvbZ6pG0qmJvAch3FCp9hkzCxRorx'
    access_token_secret = 'FB3NE8Pe8z31Sn2R4gxJfFsPFK5HA5BNAOaziHVKixZ1A'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='en').items(num_tweets)

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        print(f"Tweet: {tweet.text}")
        print(f"Sentiment: {analysis.sentiment}")
        print("\n")


latitude = 43.64599419541762
longitude = -79.38121632284623
api_key = 'AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'

mall_name = find_nearest_mall(latitude, longitude, api_key)

if mall_name:
    print(f"Analyzing sentiment for: {mall_name}")
    analyze_sentiment(mall_name, 100)
else:
    print("No mall found within the specified radius.")