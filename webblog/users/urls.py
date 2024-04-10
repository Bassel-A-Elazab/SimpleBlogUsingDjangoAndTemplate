from django.urls import path

from .views import (
    BloggerDashboardView,
    BloggerDetailView,
    BloggerListView,
    BloggerUpdateView,
)

urlpatterns = [
    path("bloggers/", BloggerListView.as_view(), name="bloggers"),
    path("bloggers/<int:pk>", BloggerDetailView.as_view(), name="blogger-detail"),
    path(
        "bloggers/<int:pk>/settings",
        BloggerUpdateView.as_view(),
        name="blogger-settings",
    ),
    path(
        "bloggers/<int:pk>/dashboard",
        BloggerDashboardView.as_view(),
        name="blogger-dashboard",
    ),
]
