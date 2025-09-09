from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

import redis
from django.conf import settings

from core.permissions import HasValidAPIKey
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .utils import get_client_ip, get_post_uuid
from .tasks import increment_post_views_task, increment_post_impressions
from .pagination import PostPagination

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, ViewPostSerializer



redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)




#Uso con APIView mas control
#Ahora usare generic view para poder aplciar Paginacion
class PostListView(GenericAPIView):
    permission_classes = [HasValidAPIKey]
    pagination_class = PostPagination

    def get_queryset(self):
        return Post.post_objects.all() 
    
    #@method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        try:
            """
            Esta aplicacion de caching Manual es mas lenta que hacer caching la vista entera, pero nos da mas modularidad y control para hacer lo que queremos
            Se lo usa para Vistas con mucha lógica o operaciones adicionales
            Si usara @cache_page, no podría actualizar Redis sin separar la logica, porque la vista ni siquiera se ejecuta cuando hay cache
            """
            #Verificamos si los datos estan en cache
            cached_posts = cache.get("post_list")
            #INcrementamos impresiones en Redis para los post del cache
            if cached_posts:

                # Si hay cache, aplicar paginación sobre el array
                page_cached = self.paginate_queryset(cached_posts)

                # Incrementar impresiones solo de la página actual      
                for post in page_cached:
                    redis_client.incr(f"post:impressions:{get_post_uuid(post)}")
                return self.get_paginated_response(page_cached)
            
            #obtener posts de la base de datos si no estan en cache
            posts = Post.post_objects.all()
            if not posts.exists():
                raise NotFound(detail="No posts found")
            
            #Serializamos los datos
            #Paginar los datos serializados

            serialized_posts = PostListSerializer(posts, many=True).data
            #Guardamos los datos en cache
            cache.set("post_list", serialized_posts, timeout=60 * 5)
            page = self.paginate_queryset(serialized_posts)



            #INcrementamos impresiones en Redis para los post del cache
            for post in page:
                redis_client.incr(f"post:impressions:{get_post_uuid(post)}")

            return self.get_paginated_response(page)
    
        except Post.DoesNotExist:
            raise NotFound(detail="No posts found")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")
        


#SOlo llamamos un objeto
class PostDetailView(APIView):
    permission_classes = [HasValidAPIKey]

    #@method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        ip_address =  get_client_ip(request)
        slug = self.kwargs.get('slug')

        try:
            #Verificamos si los datos estan en cache
            cached_post = cache.get(f"post_detail:{slug}")
            if cached_post:
                #Incrementar vistas del post
                increment_post_views_task.delay(slug, ip_address)
                return Response(cached_post)

            #obtener posts de la base de datos si no estan en cache

            #FOrma correcemtne de obetener el slug a partir de los Kwargs
            #Sirva para obtener a partir de del URL del request
            #si el slug lo defines en la URL del endpoint.
            post = Post.post_objects.get(slug=slug)
            serialized_post = PostSerializer(post).data

            #Guardar en cache
            cache.set(f"post_detail:{slug}", serialized_post, timeout=60 * 1)

            #Incrementar vistas si no estaba en cache
            increment_post_views_task.delay(post.slug, ip_address)

        except Post.DoesNotExist:
            raise NotFound(detail="The requested publicacion/post does not exist")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")
        
        return Response(serialized_post)


class PostHeadingsView(APIView):
    permission_classes = [HasValidAPIKey]

    def get(self, request, *args, **kwargs):
        post_slug = self.kwargs.get('slug')
        headings = Heading.objects.filter(post__slug=post_slug)
        serialized_headings = HeadingSerializer(headings, many=True).data
        return Response(serialized_headings)


class IncrementPostClickView(APIView):
    permission_classes = [HasValidAPIKey]

    def post(self, request):
        """
        Incrementa el contado del clicjks de un post basado en su slug
        Endpoint recibe el slug en el cuerpo de la petición (JSON).
        """
        data = request.data
        try:
            post = Post.post_objects.get(slug=data['slug'])
        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exist")

        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updateing post analytics: {str(e)}")

        return Response({
            "message": "Click incremented succesfully",
            "clicks": post_analytics.clicks
        })

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