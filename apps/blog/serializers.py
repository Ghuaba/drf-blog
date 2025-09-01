from rest_framework import serializers
from .models import Post, Heading, Category, PostView

class CategorySerializer(serializers.ModelSerializer):
    # Para GET → mostrar solo el UUID de la categoría padre
    parent = serializers.SlugRelatedField(
        read_only=True,
        slug_field="uuid"
    )
    # Para POST/PUT → enviar UUID de la categoría padre
    parent_uuid = serializers.SlugRelatedField(
        source="parent",
        slug_field="uuid",
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    class Meta:
        model = Category
        #fields = "__all__" #se llama todo
        fields = ["uuid", "parent", "parent_uuid", "name", "title", "description", "thumbnail", "slug"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
             "uuid", "name", "slug",
        ]


class ViewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields=[
            "uuid", "post", "ip_address", "created_at"
        ]


#Uso normal y sencillo de serializer
class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            "title",
            "slug",
            "level",
            "order",
        ]


class PostSerializer(serializers.ModelSerializer):
    headings = HeadingSerializer(many=True)
    category = CategoryListSerializer()
    view_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        #fields = "__all__" #se llama todo
        fields = ["uuid", "status", "view_count", "category", "title", "description", "content", "slug", "keywords", "thumbnail", "status", "headings", "created_at", "updated_at"]

    def get_view_count(self, obj):
        return obj.post_view.count()



#Para la lista en la "biblioteca" resumen, sin detalles 
class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    view_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            "uuid",
            "view_count",
            "status",
            "title",
            "description",
            "slug",
            "thumbnail",
            "category",
        ]

    def get_view_count(self, obj):
        return obj.post_view.count()

