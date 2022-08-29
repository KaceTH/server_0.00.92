from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.PostListView.as_view()),
    path('board/<int:post_id>/', views.PostEditView),
    path('notice/', views.GetNotice)
]
