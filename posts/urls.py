from . import views
from django.urls import path

urlpatterns = [
    path('<uuid:id>', views.get_specific_post_view, name='get_post'),
    path('create', views.create_post_view, name='create_post'),
    path('user/<str:uid>/all', views.get_posts_by_user_view, name='get_posts_by_user'),
    path('search', views.search_posts_view, name='search_posts'),
    path('<uuid:id>/delete', views.delete_post_view, name='delete_post'),
]