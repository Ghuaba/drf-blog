from django.urls import path, include
from .views import (
    PostListView, 
    PostDetailView, 
    PostHeadingsView, 
    IncrementPostClickView
)

urlpatterns = [
    path('post/increment_clicks/', IncrementPostClickView.as_view(), name='increment-post-click'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/headings/', PostHeadingsView.as_view(), name='post-headings-view'),
    path('posts/', PostListView.as_view(), name='post-list'),
]

