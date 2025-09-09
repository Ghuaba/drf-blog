import uuid
from django.utils.text import slugify
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field
from .utils import get_client_ip


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

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('status', '-created_at',)  # Ordena por status y luego fecha (desc)

    def __str__(self):
        return self.title
    

class PostView(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_view')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)


class PostAnalytics(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_analytics')
    views = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    click_through_rate = models.FloatField(default=0)
    avg_time_on_page = models.FloatField(default=0)


    def _update_click_through_rate(self):
        if self.impressions > 0:
            self.click_through_rate = (self.clicks / self.impressions) * 100
            self.save()
        else:
            self.click_through_rate = 0
        self.save()

    def increment_click(self):
        self.clicks +=1
        self.save()
        self._update_click_through_rate()

    
    def increment_impression(self):
        self.impressions += 1
        self.save()
        self._update_click_through_rate()

    def increment_view(self, ip_address):
        if not PostView.objects.filter(post=self.post, ip_address=ip_address).exists():
            PostView.objects.create(post=self.post, ip_address=ip_address)
            self.views +=1
            self.save()

    def __str__(self):
        return str(self.uuid)

class Heading(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='headings')
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

#cada vez que se cree un Post, también se cree su registro en PostAnalytics
@receiver(post_save, sender=Post)
def create_post_analytics(sender, instance, created, **kwargs):
    if created:
        PostAnalytics.objects.create(post=instance)