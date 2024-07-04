from configs.env import settings
from ai_celery.init_broker import is_broker_running
from ai_celery.init_redis import is_backend_running
from ai_celery.celery_app import app

if not is_backend_running():
    exit()
if not is_broker_running():
    exit()

app.conf.task_routes = {
    'tasks.audio_separator_task': {'queue': settings.AUDIO_SEPARATOR},
}

from ai_celery.audio_separator import audio_separator_task
