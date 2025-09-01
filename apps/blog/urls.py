from django.urls import path, include
from .views import PostListView, PostDetailView, PostHeadingsView


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-datail'),
    path('post/<slug:slug>/headings/', PostHeadingsView.as_view(), name='post-headings-view'),
]
