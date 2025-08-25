from django.urls import path, include
from .views import PostListView, PostDetailView


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug>', PostDetailView.as_view(), name='post-datail')
]
