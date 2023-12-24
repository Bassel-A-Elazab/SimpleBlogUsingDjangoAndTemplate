from django.urls import path

from .views import BlogListView, BlogDetailCommentView, BlogTagDetail, BlogTagList

urlpatterns = [
    path('', BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>', BlogDetailCommentView.as_view(), name='blog-detail'),
    path('tags/', BlogTagList.as_view(), name="tag-list"),
    path('tags/<int:pk>', BlogTagDetail.as_view(), name='tag-detail'),
]