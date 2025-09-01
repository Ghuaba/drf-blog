from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Post, Heading
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer


#La clase mas sencilla con ListAPIView, mas automatico
class PostListView(ListAPIView):
    #para mostrar solo los publicados , POstObjects creado por mi que se le asigan a la varaible post_objects
    queryset = Post.post_objects.all()#todos los posts publicos
    serializer_class = PostListSerializer


class PostDetailView(RetrieveAPIView):
    queryset = Post.post_objects.all()#todos los posts publicos : post_objects es la variable
    serializer_class = PostSerializer
    lookup_field = 'slug' #esto indica que el campo para buscar será `slug`

#SOlamente para otra forma de unir con headings para el post, solo llamamos a la api los headers a partir del slug
class PostHeadingsView(ListAPIView):
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug=post_slug)

        