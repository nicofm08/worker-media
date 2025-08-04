"""This module contains utility"""

from datetime import datetime
import math
import os
import time
from functools import wraps
from typing import Any

from bson import ObjectId
from worker.core.logger_custom import log
from worker.core.constants import LOG_CORE, LOG_UTILS


def execution_time(func):
    """Check the time of execution of a function"""

    @wraps(func)
    async def time_execution(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        log.info(f"{LOG_CORE} Execution time", extra={"Seconds": elapsed_time})
        return result

    return time_execution


def date_diff_mayor(date1: str, date2: str) -> bool:
    """Calculate the difference between two dates"""
    date1_parts = date1.split("-")
    date2_parts = date2.split("-")
    date1_ints = [int(i) for i in date1_parts]
    date2_ints = [int(i) for i in date2_parts]
    date1_days = date1_ints[0] * 365 + date1_ints[1] * 30 + date1_ints[2]
    date2_days = date2_ints[0] * 365 + date2_ints[1] * 30 + date2_ints[2]
    dif = date2_days - date1_days
    if dif > 0:
        return True
    return False


class UtilsCore:
    """Utils core class."""

    async def pagination(self, items, page, size):
        """Pagination function."""
        elements_quantity = len(items)
        total_pages = math.ceil(elements_quantity / size)

        if total_pages == 0:
            total_pages = 1
        range_start = (page - 1) * size
        range_end = range_start + size

        if range_end > elements_quantity:
            range_end = elements_quantity
        obj = {
            "page": page,
            "size": size,
            "last_page": total_pages,
            "total": elements_quantity,
            "response": items[range_start:range_end],
        }
        return obj

    async def apply_filters_query(self, query, filters):
        """Apply filters to a query."""
        for filter_item in filters:
            field = filter_item["field"]
            values = filter_item["value"]

            if field and values:
                filtered_values = [
                    val.strip() if isinstance(val, str) else val for val in values
                ]
                non_empty_values = [
                    val
                    for val in filtered_values
                    if (isinstance(val, str) and val.strip()) or isinstance(val, int)
                ]

                if non_empty_values:
                    query[field] = {"$in": non_empty_values}
        return query

    async def convert_objectids(self, data: Any) -> Any:
        """Convert ObjectId to string recursively."""
        if isinstance(data, dict):
            return {k: await self.convert_objectids(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [await self.convert_objectids(item) for item in data]
        elif isinstance(data, ObjectId):
            return str(data)
        else:
            return data

    async def build_update_query(self, updates):
        """Build the update query for MongoDB."""
        update_dict = {}
        for update_item in updates:
            field = update_item.get("field")
            values = update_item.get("value")
            if field and values:
                # Si el valor es una lista de un solo elemento, lo tomamos directamente
                value = values[0] if len(values) == 1 else values
                update_dict[field] = value
        if update_dict:
            return {"$set": update_dict}
        return {}

    def add_metadata(self, file_path: str) -> dict:
        """Add metadata to a file"""
        log.info(f"{LOG_UTILS} Adding metadata to file: {file_path}")
        return {
            "worker": "media_worker",
            "date_processed": datetime.now().isoformat(),
            "file_path": file_path,
        }

    async def clear_file(self, file_path: str) -> None:
        """Clear a file."""
        log.info(f"{LOG_UTILS} Clearing file: {file_path}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
