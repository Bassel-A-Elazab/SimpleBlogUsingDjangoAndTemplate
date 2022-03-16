from django.urls import path

from .views import BloggerListView, BloggerDetailView

urlpatterns = [
    path('bloggers/', BloggerListView.as_view(), name='bloggers'),
    path('bloggers/<int:pk>', BloggerDetailView.as_view(), name='blogger-detail'),
]