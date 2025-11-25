"""Request models for API."""
from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response model for file upload."""
    job_id: str
    status: str
    message: str
