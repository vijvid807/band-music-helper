"""AMT (Automatic Music Transcription) API endpoints."""
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from loguru import logger

from src.services.job_service import JobService, JobType, JobStatus
from src.services.file_service import FileService
from src.pipeline.amt_pipeline import AMTPipeline
from src.core.dependencies import get_job_service, get_file_service, get_amt_pipeline
from src.api.models.requests import UploadResponse
from src.api.models.responses import JobStatusResponse
from src.config.settings import settings

router = APIRouter()


async def process_amt_job(
    job_id: str,
    upload_path: Path,
    job_service: JobService,
    amt_pipeline: AMTPipeline
):
    """Process AMT job asynchronously."""
    try:
        logger.info(f"Starting AMT processing for job: {job_id}")
        
        def status_callback(jid: str, status_data: dict):
            """Callback for pipeline status updates."""
            job_service.update_job(jid, **status_data)
        
        # Run pipeline
        output_path = await amt_pipeline.process(
            upload_path,
            job_id,
            status_callback=status_callback
        )
        
        # Mark as completed
        job_service.mark_completed(job_id, str(output_path))
        logger.info(f"AMT job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"AMT job {job_id} failed: {e}")
        job_service.mark_failed(job_id, str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_audio_for_amt(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    job_service: JobService = Depends(get_job_service),
    file_service: FileService = Depends(get_file_service),
    amt_pipeline: AMTPipeline = Depends(get_amt_pipeline)
):
    """
    Upload an audio file for Automatic Music Transcription.
    Returns a job ID for tracking the conversion process.
    """
    try:
        # Validate file type
        if not file_service.validate_file_extension(file.filename, settings.amt_allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(settings.amt_allowed_extensions)}"
            )
        
        # Save uploaded file
        job_id, upload_path = file_service.save_upload(file.file, file.filename)
        
        # Create job
        job_service.create_job(
            job_id=job_id,
            job_type=JobType.AMT,
            filename=file.filename,
            upload_path=str(upload_path)
        )
        
        logger.info(f"AMT job {job_id} created for file: {file.filename}")
        
        # Start async processing
        background_tasks.add_task(
            process_amt_job,
            job_id,
            upload_path,
            job_service,
            amt_pipeline
        )
        
        return UploadResponse(
            job_id=job_id,
            status="uploaded",
            message="File uploaded successfully. Processing started."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AMT upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_amt_status(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """Get the status of an AMT conversion job."""
    job = job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(**job.to_dict())


@router.get("/download/{job_id}")
async def download_amt_result(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """Download the generated PDF score."""
    job = job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Job is not complete. Current status: {job.status.value}"
        )
    
    output_path = Path(job.output_path)
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"{Path(job.filename).stem}_score.pdf"
    )
