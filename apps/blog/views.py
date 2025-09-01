from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_client_ip

from .models import Post, Heading, PostView
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, ViewPostSerializer


#Uso con APIView
class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.post_objects.all()
        serialized_posts = PostListSerializer(posts, many=True).data
        return Response(serialized_posts)


class PostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        post = Post.post_objects.get(slug=slug)
        serialized_post = PostSerializer(post).data
        #Para hacer conteo de visualizaciones
        client_ip =  get_client_ip(request)
        if PostView.objects.filter(post=post, ip_address=client_ip).exists():
            return Response(serialized_post)

        PostView.objects.create(post=post, ip_address=client_ip)
        return Response(serialized_post)


class PostHeadingsView(APIView):
    def get(self, request, *args, **kwargs):
        post_slug = self.kwargs.get('slug')
        headings = Heading.objects.filter(post__slug=post_slug)
        serialized_headings = HeadingSerializer(headings, many=True).data
        return Response(serialized_headings)


#Realizado con GenerisAPIView
# #La clase mas sencilla con ListAPIView, mas automatico
# class PostListView(ListAPIView):
#     #para mostrar solo los publicados , POstObjects creado por mi que se le asigan a la varaible post_objects
#     queryset = Post.post_objects.all()#todos los posts publicos
#     serializer_class = PostListSerializer


# class PostDetailView(RetrieveAPIView):
#     queryset = Post.post_objects.all()#todos los posts publicos : post_objects es la variable
#     serializer_class = PostSerializer
#     lookup_field = 'slug' #esto indica que el campo para buscar será `slug`

#SOlamente para otra forma de unir con headings para el post, solo llamamos a la api los headers a partir del slug
# class PostHeadingsView(ListAPIView):
#     serializer_class = HeadingSerializer

#     def get_queryset(self):
#         post_slug = self.kwargs.get("slug")
#         return Heading.objects.filter(post__slug=post_slug)

        