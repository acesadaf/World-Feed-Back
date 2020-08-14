from django.urls import path
from backend import views
urlpatterns = [
    path("get_tweet", views.get_tweet, name="get_tweet"),
    path("get_news", views.get_news, name="get_news"),
    path("get_videos", views.get_videos, name="get_videos")]
