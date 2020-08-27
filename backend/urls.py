from django.urls import path
from backend import views
urlpatterns = [
    path("get_tweet", views.get_tweet, name="get_tweet"),
]
