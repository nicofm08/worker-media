"""S3 model"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class S3DB(BaseModel):
    """S3 model"""
    url: Optional[str] = ""
    key: Optional[str] = ""
    filename: Optional[str] = ""
    expires_at: Optional[datetime] = None
    extra_info: Optional[dict] = {}