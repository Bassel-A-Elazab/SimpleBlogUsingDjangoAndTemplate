from django.urls import path

from .views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailCommentView,
    BlogListView,
    BlogTagDetail,
    BlogTagList,
    BlogUpdateView,
)

urlpatterns = [
    path("", BlogListView.as_view(), name="blogs"),
    path("blogs/<int:pk>", BlogDetailCommentView.as_view(), name="blog-detail"),
    path("blog/new/", BlogCreateView.as_view(), name="blog-new"),
    path("blog/<int:pk>/update", BlogUpdateView.as_view(), name="blog-update"),
    path("blogs/<int:pk>/delete", BlogDeleteView.as_view(), name="blog-delete"),
    path("tags/", BlogTagList.as_view(), name="tag-list"),
    path("tags/<int:pk>", BlogTagDetail.as_view(), name="tag-detail"),
]
