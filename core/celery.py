from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

"""
Configrate timezone
"""
app.conf.enable_utc = False
app.conf.update(timezone="America/Bogota")

"""
Usando string el worker no necesita serializar
"""
app.config_from_object("django.conf:settings", namespace="CELERY")

#Para que celery autodescubra las tareas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#Probando tarea de celery
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")