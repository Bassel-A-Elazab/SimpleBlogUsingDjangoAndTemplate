from django.urls import path

from .views import BlogListView, BlogDetailCommentView

urlpatterns = [
    path('', BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>', BlogDetailCommentView.as_view(), name='blog-detail'),
]