"""Response models for API."""
from pydantic import BaseModel
from typing import Optional


class JobStatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    type: str
    status: str
    filename: str
    upload_path: str
    output_path: Optional[str] = None
    error: Optional[str] = None
    step: Optional[str] = None
    progress: int = 0
    created_at: str
    updated_at: str
