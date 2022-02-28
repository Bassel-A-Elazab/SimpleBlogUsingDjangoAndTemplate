from django.urls import path

from .views import BlogCommentCreateView, BlogListView, BlogDetailView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blogs/<pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<pk>/comment', BlogCommentCreateView.as_view(), name='add-comment'),
]