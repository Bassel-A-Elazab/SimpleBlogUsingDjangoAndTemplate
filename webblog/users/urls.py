from django.urls import path

# app_name = 'users'
from .views import BloggerListView

urlpatterns = [
    path('bloggers/', BloggerListView.as_view(), name='bloggers'),
]