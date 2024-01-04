from . import views
from django.urls import path

urlpatterns = [
    path('post/<uuid:post_id>', views.like_post_view, name='like_posts'),
    path('comment/<uuid:comment_id>', views.like_comment_view, name='like_comments'),
    path('post/<uuid:post_id>/unlike', views.unlike_post_view, name='unlike_posts'),
    path('comment/<uuid:comment_id>/unlike', views.unlike_comment_view, name='unlike_comments'),
]