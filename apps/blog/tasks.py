from celery import shared_task

import logging
import redis
from django.conf import settings
from .models import PostAnalytics

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

logger = logging.getLogger(__name__)

#siempre para crear una tarea de celery, este decorador
@shared_task
def increment_post_impressions(post_id):
    """
    Incrementa las impresiones del post asociado
    """
    try:
        analistycs, created = PostAnalytics.objects.get_or_create(post__id=post_id)
        analistycs.increment_impression()
    except Exception as e:
        logger.info(f"Error incrememnted impresison for  POST ID {post_id}: {str(e)}")


@shared_task
def sync_impressions_to_db():
    """
    Sincronizar las impresiones almacenadas en redis con la base de datos
    """
    keys = redis_client.keys("post:impressions:*")
    for key in keys:
        try:
            post_id = key.decode("utf-8").split(":")[-1]
            impressions = int(redis_client.get(key))

            analytics, created = PostAnalytics.objects.get_or_create(post__id=post_id)
            analytics.impressions += impressions
            analytics.save()

            redis_client.delete(key)
        except Exception as e:
            logger.info(f"Error syncing impressions for  {key}: {str(e)}")
