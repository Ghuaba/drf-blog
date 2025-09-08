from celery import shared_task

import logging

from .models import PostAnalytics

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