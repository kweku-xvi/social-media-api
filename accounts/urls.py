from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.sign_up_view, name='signup_user'),
    path('verify-user', views.verify_user_view, name='verify_user'),
    path('login', views.login_view, name='login_user'),
    path('users', views.get_users_view, name='get_users'),
    path('password-reset', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('search', views.search_user_view, name='search_users'),
    path('<str:user_id>/update', views.update_user_details_view, name='update_user_details')
]