from . import views
from django.urls import path

urlpatterns = [
    path('<uuid:comment_id>', views.get_specific_comment_view, name='get_comment'),
    path('<uuid:post_id>/add', views.add_comment_view, name='add_comment'),
    path('post/<uuid:post_id>/all', views.get_comments_on_post_view, name='get_comments_on_post'),
    path('user/<str:uid>/all', views.get_all_comments_by_user_view, name='get_comments_by_user'),
    path('<uuid:comment_id>/delete', views.delete_comment_view, name='delete_comment'),
]