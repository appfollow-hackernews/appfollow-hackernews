from django.contrib import admin
from django.urls import path

from hackernews import views, models


urlpatterns = [
    path('posts', views.PostListView.as_view(), name='posts'),
    path('update', views.update, name='update'),
]
