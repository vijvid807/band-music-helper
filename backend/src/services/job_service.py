"""Job service for managing conversion jobs."""
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from loguru import logger


class JobType(str, Enum):
    """Job type enumeration."""
    OMR = "omr"
    AMT = "amt"


class JobStatus(str, Enum):
    """Job status enumeration."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    """Job data class."""
    job_id: str
    type: JobType
    status: JobStatus
    filename: str
    upload_path: str
    output_path: Optional[str] = None
    error: Optional[str] = None
    step: Optional[str] = None
    progress: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """Convert job to dictionary."""
        return {
            "job_id": self.job_id,
            "type": self.type.value,
            "status": self.status.value,
            "filename": self.filename,
            "upload_path": self.upload_path,
            "output_path": self.output_path,
            "error": self.error,
            "step": self.step,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class JobService:
    """Service for managing conversion jobs."""
    
    def __init__(self):
        """Initialize job service."""
        self._jobs: Dict[str, Job] = {}
        logger.info("JobService initialized")
    
    def create_job(
        self,
        job_id: str,
        job_type: JobType,
        filename: str,
        upload_path: str
    ) -> Job:
        """Create a new job."""
        job = Job(
            job_id=job_id,
            type=job_type,
            status=JobStatus.UPLOADED,
            filename=filename,
            upload_path=upload_path
        )
        self._jobs[job_id] = job
        logger.info(f"Created job {job_id} of type {job_type.value}")
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> Optional[Job]:
        """Update job with new data."""
        job = self._jobs.get(job_id)
        if job:
            for key, value in kwargs.items():
                if hasattr(job, key):
                    setattr(job, key, value)
            job.updated_at = datetime.utcnow()
            logger.debug(f"Updated job {job_id}: {kwargs}")
        return job
    
    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        step: Optional[str] = None,
        progress: Optional[int] = None,
        error: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Optional[Job]:
        """Update job status."""
        updates = {"status": status}
        if step is not None:
            updates["step"] = step
        if progress is not None:
            updates["progress"] = progress
        if error is not None:
            updates["error"] = error
        if output_path is not None:
            updates["output_path"] = output_path
        
        return self.update_job(job_id, **updates)
    
    def mark_processing(self, job_id: str, step: str, progress: int) -> Optional[Job]:
        """Mark job as processing."""
        return self.update_status(
            job_id,
            JobStatus.PROCESSING,
            step=step,
            progress=progress
        )
    
    def mark_completed(self, job_id: str, output_path: str) -> Optional[Job]:
        """Mark job as completed."""
        return self.update_status(
            job_id,
            JobStatus.COMPLETED,
            progress=100,
            output_path=output_path
        )
    
    def mark_failed(self, job_id: str, error: str) -> Optional[Job]:
        """Mark job as failed."""
        return self.update_status(
            job_id,
            JobStatus.FAILED,
            error=error
        )
    
    def delete_job(self, job_id: str) -> bool:
        """Delete job by ID."""
        if job_id in self._jobs:
            del self._jobs[job_id]
            logger.info(f"Deleted job {job_id}")
            return True
        return False
    
    def list_jobs(self, job_type: Optional[JobType] = None) -> list[Job]:
        """List all jobs, optionally filtered by type."""
        jobs = list(self._jobs.values())
        if job_type:
            jobs = [j for j in jobs if j.type == job_type]
        return jobs
