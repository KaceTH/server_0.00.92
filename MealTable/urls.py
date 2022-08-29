from django.urls import path

from . import views

urlpatterns = [
    path('', views.getmeal.as_view()),
    path('update/', views.MealListView.as_view())
]
