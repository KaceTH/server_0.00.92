from django.urls import path

from .view_lists import verificateView, loginView, views

urlpatterns = [
    path('login/', loginView.login),
    path('users/', views.signUp),
    path('users/<str:username>/', views.user_setting),
    path('users/<str:username>/change/', views.change),
    path('email_pass/<str:username>/', verificateView.email_verification),
    path('email_pass/<str:username>/change/', views.change_pw_verification)
]