"""Process media task."""

from worker.celery_app import celery
from worker.tasks.process_image import process_image_task
from worker.tasks.process_video import process_video_task
from worker.core.logger_custom import log
from worker.core.constants import LOG_TASK


@celery.task(name="process_media")
def process_media(event: dict):
    """Process media task."""
    log.info(f"{LOG_TASK} Processing media: {event}")
    if event.get("media_type") == "IMAGE":
        process_image_task.delay(event)
    elif event.get("media_type") == "VIDEO":
        process_video_task.delay(event)
    else:
        log.warning(f"{LOG_TASK} Type unknown: {event.get('media_type')}")
