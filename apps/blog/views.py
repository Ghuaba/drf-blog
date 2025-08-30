from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Post
from .serializers import PostListSerializer, PostSerializer


#La clase mas sencilla con ListAPIView, mas automatico
class PostListView(ListAPIView):
    #para mostrar solo los publicados , POstObjects creado por mi que se le asigan a la varaible post_objects
    queryset = Post.post_objects.all()
    serializer_class = PostListSerializer


class PostDetailView(RetrieveAPIView):
    queryset = Post.post_objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'