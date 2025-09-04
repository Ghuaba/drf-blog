from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, ViewPostSerializer
from .utils import get_client_ip


#Uso con APIView mas control
class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.post_objects.all()
            if not posts.exists():
                raise NotFound(detail="No posts found")
            
            serialized_posts = PostListSerializer(posts, many=True).data
        except Post.DoesNotExist:
            raise NotFound(detail="No posts found")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")
        
        return Response(serialized_posts)


class PostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #FOrma correcemtne de obetener el slug a partir de los Kwargs
            slug = self.kwargs.get('slug')
            post = Post.post_objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="The requested publicacion/post does not exist")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")
        
        serialized_post = PostSerializer(post).data
        #Para hacer conteo de visualizaciones
        #Incrementa post view count
        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="Analytics data for thuis post does not exist")
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updateing post analytics: {str(e)}")
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

        