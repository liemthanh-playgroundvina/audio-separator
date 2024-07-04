import json
import logging
import os.path
import shutil
from datetime import datetime

from celery import Task
from ai_celery.celery_app import app
from configs.env import settings
from ai_celery.common import Celery_RedisClient, CommonCeleryService

import torch
from interface import separate_audio


class AudioSeparatorTask(Task):
    """
    Abstraction of Celery's Task class to support AI Audio Separator
    """
    abstract = True

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


@app.task(
    bind=True,
    base=AudioSeparatorTask,
    name="{query}.{task_name}".format(
        query=settings.AI_QUERY_NAME,
        task_name=settings.AUDIO_SEPARATOR
    ),
    queue=settings.AUDIO_SEPARATOR
)
def audio_separator_task(self, task_id: str, data: bytes, task_request: bytes, file: bytes):
    """
    Service Audio Separator tasks

    task_request example:
        request: {
            "level": "basic"
        }
        file: {'content_type': 'audio/mpeg', 'filename': 'static/public/ai_cover_gen/voice.mp3'}
    """
    print(f"============= Audio Separator task {task_id}: Started ===================")
    try:
        # Load data
        data = json.loads(data)
        request = json.loads(task_request)
        file = json.loads(file)
        Celery_RedisClient.started(task_id, data)

        # Check task removed
        Celery_RedisClient.check_task_removed(task_id)

        # Predict
        audio_file = file.get('filename').split("/")[-1]
        audio_file = "/app/static/public/ai_cover_gen/" + audio_file
        output_dir, output, time_execute = separate_audio(audio_file, request.get('level'))

        # Save s3
        urls = {
            "instrumental": CommonCeleryService.fast_upload_s3_files(output["instrumental"], settings.AUDIO_SEPARATOR),
            "vocals": CommonCeleryService.fast_upload_s3_files(output["vocals"], settings.AUDIO_SEPARATOR),
        }

        # Successful
        metadata = {
            "task": settings.AUDIO_SEPARATOR,
            "tool": "local",
            "model": "python-audio-separator",
            "usage": None,
            "time_execute": time_execute,
        }
        response = {"urls": urls, "metadata": metadata}
        Celery_RedisClient.success(task_id, data, response)

        try:
            shutil.rmtree(output_dir)
        except:
            pass

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return

    except ValueError as e:
        logging.getLogger().error(str(e), exc_info=True)
        err = {'code': "400", 'message': str(e).split('!')[0].strip()}
        Celery_RedisClient.failed(task_id, data, err)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return

    except Exception as e:
        logging.getLogger().error(str(e), exc_info=True)
        err = {'code': "500", 'message': "Internal Server Error"}
        Celery_RedisClient.failed(task_id, data, err)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return
