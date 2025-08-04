"""Custom logger for the application."""

import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DDTHH:mm:ss}</green> | <level>{level}</level> | "
    "<yellow>{"
    "name}</yellow> | <cyan>{function}</cyan> | <level>{message}</level> | {"
    "extra}",
    # Ensure that logs are not kept in memory (this is default behavior, just for clarity)
    backtrace=False,
    diagnose=False,
)

log = logger
