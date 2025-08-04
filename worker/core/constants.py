"""This module contains the constants used in the application."""

import os
import json
import requests
from dotenv import load_dotenv
from worker.core.logger_custom import log

load_dotenv()


def get_config_server():
    """Get configuration from config server."""
    log.info("Getting configuration from config server")
    url = os.environ.get("CONFIG_SERVER_URL", "http://localhost:8080/api/v1/config")
    log.info(f"URL: {url}")
    log.info(f'Repository: {os.environ.get("REPOSITORY")}')
    log.info(f'Branch: {os.environ.get("BRANCH")}')
    log.info(f'Component: {os.environ.get("COMPONENT")}')
    log.info(f'TKS: {os.environ.get("TKS")}')
    headers = {"Content-Type": "application/json"}
    data = {
        "repository": os.environ.get("REPOSITORY"),
        "branch": os.environ.get("BRANCH"),
        "component": os.environ.get("COMPONENT"),
        "tks": os.environ.get("TKS"),
    }
    log.info(f"Data: {data}")
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    log.info(f"Response: {response.json()}")
    return response.json()


config_server = get_config_server()
HTTP_TIMEOUT = config_server["HTTP_TIMEOUT"]
MONGO_URI = config_server["MONGO_URI"]
AWS_ACCESS_KEY_ID = config_server["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = config_server["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = config_server["AWS_REGION"]
AWS_BUCKET_NAME = config_server["AWS_BUCKET_NAME"]
REDIS_HOST = config_server["REDIS_HOST"]
REDIS_PORT = config_server["REDIS_PORT"]
REDIS_DB = config_server["REDIS_DB"]
REDIS_PASSWORD = config_server["REDIS_PASSWORD"]
REDIS_DEFAULT_EXPIRATION_TIME = config_server["REDIS_DEFAULT_EXPIRATION_TIME"]
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
REDIS_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
MYSQL_HOST = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""
LOG_INIT = "[WORKER_INI]"
LOG_FINOK = "[WORKER_FINOK]"
LOG_FINERROR = "[WORKER_ENDERROR]"
LOG_DATA = "[DATA]"
LOG_HANDLER = "[REQ_BODY]"
LOG_SERVICE = "[SERVICE]"
LOG_USECASE = "[USE_CASE]"
LOG_REPOSITORY = "[REPOSITORY]"
LOG_CORE = "[CORE]"
LOG_MIDDLEWARE = "[MIDDLEWARE]"
LOG_TASK = "[TASK]"
LOG_UTILS = "[UTILS]"


def get_constants():
    """Get constants function to call in health endpoint."""
    return {
        "MYSQL_HOST": MYSQL_HOST,
        "MYSQL_USER": MYSQL_USER,
        "MYSQL_PASSWORD": MYSQL_PASSWORD,
        "MYSQL_DATABASE": MYSQL_DATABASE,
        "MONGO_URI": MONGO_URI,
        "REDIS_HOST": REDIS_HOST,
        "REDIS_PORT": REDIS_PORT,
        "REDIS_DB": REDIS_DB,
        "REDIS_PASSWORD": REDIS_PASSWORD,
        "LOG_INIT": LOG_INIT,
        "LOG_FINOK": LOG_FINOK,
        "LOG_FINERROR": LOG_FINERROR,
        "LOG_DATA": LOG_DATA,
        "LOG_HANDLER": LOG_HANDLER,
        "LOG_SERVICE": LOG_SERVICE,
        "LOG_USECASE": LOG_USECASE,
        "LOG_REPOSITORY": LOG_REPOSITORY,
        "LOG_CORE": LOG_CORE,
        "LOG_MIDDLEWARE": LOG_MIDDLEWARE,
        "HTTP_TIMEOUT": HTTP_TIMEOUT,
        "LOG_TASK": LOG_TASK,
        "LOG_UTILS": LOG_UTILS,
    }