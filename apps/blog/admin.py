from django.contrib import admin
from django import forms
from .models import Post, Heading, Category
from django_ckeditor_5.widgets import CKEditor5Widget


#Registrar categorias
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    oredering = ('name')
    readonly_fields = ('uuid',)

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Post
        fields = '__all__'


#Para registrar Publicaciones
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at',)
    search_fields = ('title', 'description', 'content', 'keywords', 'slug',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category', 'updated_at',)
    ordering = ('-created_at',)
    readonly_fields = ('uuid', 'created_at', 'updated_at',)
    fieldsets =  (
        ('General Information', {
            'fields': ('title', 'description', 'content', 'thumbnail', 'keywords', 'slug', 'category',)
        }),
        ('Status & Dates', {
            'fields': ('status','created_at', 'updated_at',)
        }),
        ('ID', {
            'fields': ('uuid',)
        }),
    )


@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ('title', 'post', 'level', 'order',)
    search_fields = ('title', 'post__title')
    list_filter = ('level', 'post')
    oredering = ('post', 'order')
    prepopulated_fields = {'slug': ('title',)}

