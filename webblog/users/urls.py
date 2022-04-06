from django.urls import path

from .views import BloggerListView, BloggerDetailView, BloggerUpdateView

urlpatterns = [
    path('bloggers/', BloggerListView.as_view(), name='bloggers'),
    path('bloggers/<int:pk>', BloggerDetailView.as_view(), name='blogger-detail'),
    path('bloggers/<int:pk>/settings', BloggerUpdateView.as_view(), name='blogger-settings')
]