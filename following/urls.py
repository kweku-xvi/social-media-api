from . import views
from django.urls import path

urlpatterns = [
    path('<str:uid>/follow', views.follow_user_view, name='follow_user'),
    path('<str:uid>/unfollow', views.unfollow_user_view, name='unfollow_user'),
]