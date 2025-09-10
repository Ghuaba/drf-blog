from celery import shared_task

import logging
import redis
from django.conf import settings
from .models import PostAnalytics, Post

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

logger = logging.getLogger(__name__)

#siempre para crear una tarea de celery, este decorador
@shared_task
def increment_post_impressions(post_uuid):
    """
    Incrementa las impresiones del post asociado
    """
    try:
        analitycs, created = PostAnalytics.objects.get_or_create(post__uuid=post_uuid)
        analitycs.increment_impression()
    except Exception as e:
        logger.info(f"Error incrememnted impresison for  POST ID {post_uuid}: {str(e)}")


@shared_task
def increment_post_views_task(slug, ip_address):
    """
    INcrementa las vistas de un post
    """
    #Incrementa post view count
    try:
        post = Post.objects.get(slug=slug)
        post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
        post_analytics.increment_view(ip_address)
    except Exception as e:
        logger.info(f"An error ocurred while updateing post analytics: {str(e)}")


@shared_task
def sync_impressions_to_db():
    """
    Sincronizar las impresiones almacenadas en redis con la base de datos
    """
    keys = redis_client.keys("post:impressions:*")
    for key in keys:
        try:
            post_uuid = key.decode("utf-8").split(":")[-1]
            impressions = int(redis_client.get(key))

            # Obtener el Post real
            post = Post.objects.filter(uuid=post_uuid).first()
            if not post:
                logger.warning(f"Post with UUID {post_uuid} not found, skipping.")
                redis_client.delete(key)
                continue

            analytics, created = PostAnalytics.objects.get_or_create(post=post)
            analytics.impressions += impressions
            analytics.save()
            
            analytics._update_click_through_rate()

            redis_client.delete(key)
        except Exception as e:
            logger.info(f"Error syncing impressions for  {key}: {str(e)}")


