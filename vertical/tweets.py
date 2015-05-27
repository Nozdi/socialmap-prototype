from datetime import (
    datetime,
    timedelta
)
import tweepy
import pandas as pd
from pygeocoder import Geocoder

from config import (
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)

TWITTER_AUTH = tweepy.OAuthHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET
)
TWITTER_AUTH.set_access_token(
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)


def setup_twitter_api():
    return tweepy.API(
        TWITTER_AUTH,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
    )


def search(api, place):
    lat, lng = Geocoder.geocode(place)[0].coordinates
    geocode = "{},{},{}km".format(lat, lng, 10)
    since_date = datetime.now() - timedelta(days=1)
    str_date = since_date.strftime("%Y-%m-%d")
    cur = tweepy.Cursor(
        api.search,
        geocode=geocode,
        since=str_date,
        count=100,
    )

    for tweet in cur.items():
        yield tweet._json


if __name__ == '__main__':
    df = pd.DataFrame(search(setup_twitter_api(), "London"))
    df.to_json("data.json")
