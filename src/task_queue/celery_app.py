from celery import Celery
from settings.config import CeleryConfig

app = Celery("tasks")

app.config_from_object(CeleryConfig)

app.autodiscover_tasks(["task_queue.tasks"])
