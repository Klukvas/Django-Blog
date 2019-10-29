from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.ShowNewView.as_view(), name='blog-home'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-datail'),
    path('news/add/', views.CreateNewsView.as_view(), name='news-add'),
    path('contact', views.contacti, name='blog-contact'),
    path('news/<int:pk>/delete/', views.DeleteNewsView.as_view(), name='news-delete'),
    path('news/<int:pk>/update/', views.UpdateNewsView.as_view(), name='news-update'),
    path('news/<str:username>/', views.UserAllNewsView.as_view(), name='user-news'),
]
