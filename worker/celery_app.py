"""Celery app configuration."""

from celery import Celery
from worker.core.constants import LOG_CORE, REDIS_URL, REDIS_BACKEND
from worker.core.logger_custom import log

celery = Celery("media_worker", broker=REDIS_URL, backend=REDIS_BACKEND)
log.info(f"{LOG_CORE} Celery app initialized")
celery.autodiscover_tasks(["worker.tasks"])
