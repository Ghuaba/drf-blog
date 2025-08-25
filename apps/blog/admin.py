from django.contrib import admin
from .models import Post, Heading, Category

#Registrar categorias
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    oredering = ('name')
    readonly_fields = ('uuid',)

#Para registrar Publicaciones
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category', 'updated_at',)
    oredering = ('-created_at',)
    readonly_fields = ('uuid', 'created_at', 'updated_at',)
    fieldsets =  (
        ('General Information', {
            'fields': ('title', 'description', 'content', 'thumbnail', 'keywords', 'slug', 'category')
        }),
        ('Status & Dates', {
            'fields': ('status','created_at', 'updated_at')
        }),
        ('ID', {
            'fields': ('uuid',)
        }),
    )
