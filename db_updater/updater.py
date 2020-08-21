from datetime import datetime, timezone
import os
from backend.models import CityTweetCache, CountryTweetCache

from apscheduler.schedulers.background import BackgroundScheduler


def update():
    print("updating")
    states = CityTweetCache.objects.all()

    for s in states:
        # print(s.cache_time, datetime.now(timezone.utc))
        delta = datetime.now(timezone.utc) - s.cache_time
        # print(delta.seconds)
        if (delta.seconds)/60 > 0.5:
            city, country = s.city, s.country
            entry_to_delete = CityTweetCache.objects.get(
                city=city, country=country)
            entry_to_delete.delete()

    countries = CountryTweetCache.objects.all()

    for c in countries:
        # print("here??")
        delta = datetime.now(timezone.utc) - c.cache_time
        # print(delta.seconds)
        if (delta.seconds)/60 > 0.5:
            country = c.country
            entry_to_delete = CountryTweetCache.objects.get(country=country)
            entry_to_delete.delete()


def start():
    print("Starting scheduler..")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update, trigger='interval', minutes=0.1)
    scheduler.start()
    scheduler_active = True
