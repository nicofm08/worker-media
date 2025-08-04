import asyncio

from celery.app import shared_task
from worker.celery_app import celery
from worker.core.s3_client import S3Client
from worker.core.mongo import MongoClient
from worker.core.utils import UtilsCore
from worker.core.constants import LOG_TASK
from worker.core.logger_custom import log

@shared_task(name="process_image")
def process_image_task(event: dict):
    asyncio.run(_process_image_task(event))


async def _process_image_task(event: dict):
    log.info(f"{LOG_TASK} Processing image: {event}")
    s3_key = event.get("s3_filename")
    media_id = event.get("s3_filename")

    s3_client = S3Client()
    mongo_client = MongoClient(db="api-media", collection="media")
    utils_core = UtilsCore()

    local_path = await s3_client.download_file_small(s3_key)
    processed_path = utils_core.add_metadata(s3_key)
    await mongo_client.update_one(
    {"s3_filename": media_id},
    {"$set": {
        "status": "PROCESSED",
        "filename_processed": processed_path
    }}
)
    log.info(f"{LOG_TASK} Media updated: {media_id}")
    return True