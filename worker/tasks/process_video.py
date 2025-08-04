import asyncio

from celery.app import shared_task
from worker.celery_app import celery
from worker.core.s3_client import S3Client
from worker.core.mongo import MongoClient
from worker.core.utils import UtilsCore
from worker.core.constants import LOG_TASK
from worker.core.logger_custom import log

@shared_task(name="process_video")
def process_video_task(event: dict):
    asyncio.run(_process_video_task(event))


async def _process_video_task(event: dict):
    log.info(f"{LOG_TASK} Processing video: {event}")
    s3_key = event.get("s3_filename")
    media_id = event.get("s3_filename")

    s3_client = S3Client()
    mongo_client = MongoClient(db="api-media", collection="media")
    utils_core = UtilsCore()

    local_path = s3_client.download_file_large(s3_key)
    processed_path = utils_core.add_metadata(local_path)

    await mongo_client.update_one(
        {"s3_filename": media_id},
        {"status": "PROCESSED", "filename_processed": processed_path}
    )
    log.info(f"{LOG_TASK} Media updated: {media_id}")
    await utils_core.clear_file(local_path)
    return True