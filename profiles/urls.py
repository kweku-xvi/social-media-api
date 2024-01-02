from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_user_profile_view, name='user_profile'),
    path('<str:user_id>/update', views.update_profile_view, name='update_profile'),
]