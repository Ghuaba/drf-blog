import uuid
from django.utils.text import slugify
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field



def blog_thumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)


###################################################
#EL primer tipo de campo para la db, el segundo para el frontend, llamamos la constantne, es global
class PostStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


def category_thumbnail_directory(instance, filename):
    return "blog_categories/{0}/{1}".format(instance.name, filename)

class Category(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    thumbnail = models.ImageField(upload_to = blog_thumbnail_directory, null=True, blank=True)
    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.name
"""
Otra forma de definir choices sin usar TextChoices
postStatus = (
    ("draft", "Draft"),
    ("published", "Published")
)

La mejor manera es usar TextChoices
Otra alternativa es usar una Lista de tuplas ya que es inmutable
postStatus = [
    ("draft", "Draft"),
    ("published", "Published")
]
"""
########################################################



class Post(models.Model):
#Solo se mostraran al llamado los PUBLISHED
    class PostObjects(models.Manager):
        #Todas las funciones dentro de una clase llevan self
        def get_queryset(self):
            return super().get_queryset().filter(status=PostStatus.PUBLISHED)
        
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=90)
    description = models.CharField(max_length=128)
    #content = models.TextField()
    content = CKEditor5Field('Content', config_name='default')

    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length = 128)
    thumbnail = models.ImageField(upload_to=blog_thumbnail_directory)
    #author = 
    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
    objects = models.Manager() #Default manager
    post_objects = PostObjects()  # Custom manager for published posts
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('status', '-created_at',)  # Ordena por status y luego fecha (desc)


    def __str__(self):
        return self.title
    
class Heading(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='headings')
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length = 255)
    level = models.IntegerField(
        choices=(
            (1, 'H1'),
            (2, 'H2'),
            (3, 'H3'),
            (4, 'H4'),
            (5, 'H5'),
            (6, 'H6'),
        )
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def save(self, *argas, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*argas, **kwargs)