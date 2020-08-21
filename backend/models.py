from django.db import models
from django.contrib.postgres.fields import ArrayField


class CountryTweetCache(models.Model):
    country = models.CharField(unique=True, max_length=100)
    tweets = ArrayField(models.CharField(max_length=200))
    cache_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.country, self.tweets}"


class CityTweetCache(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tweets = ArrayField(models.CharField(max_length=200))
    cache_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = (('city', 'country'),)

    def __str__(self):
        return f"{self.city, self.country, self.tweets}"
    # Create your models here.
