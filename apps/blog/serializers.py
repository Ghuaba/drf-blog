from rest_framework import serializers
from .models import Post, Heading, Category

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

class PostSerializer(serializers.ModelSerializer):
    
    # Para GET → mostrar datos completos de la categoría
    category = CategorySerializer(read_only=True)
    # Para POST/PUT → recibir UUID del cliente
    category_uuid = serializers.SlugRelatedField(
        source="category",
        slug_field="uuid",
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = Post
        fields = ["uuid", "title", "description", "slug", "thumbnail", "category", "category_uuid"]


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            "title",
            "slug",
            "level",
            "order",
        ]

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "uuid",
            "title",
            "description",
            "slug",
            "thumbnail",
            "category",
        ]

