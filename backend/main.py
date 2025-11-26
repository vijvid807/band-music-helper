"""FastAPI application for Band Music conversion platform."""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict
from pathlib import Path
import uuid
import shutil
import asyncio
from loguru import logger

from src.pipeline.omr_pipeline import OMRPipeline
from src.pipeline.amt_pipeline import AMTPipeline

# Configure logging
logger.add("logs/app.log", rotation="500 MB", level="INFO")

# Initialize FastAPI app
app = FastAPI(
    title="Band Music API",
    description="Convert sheet music images to audio and audio files to sheet music",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Storage for job status
jobs: Dict[str, Dict] = {}

# Initialize pipelines
omr_pipeline = OMRPipeline()
amt_pipeline = AMTPipeline()


@app.get("/favicon.ico")
async def favicon():
    """Return 204 No Content for favicon requests."""
    return JSONResponse(status_code=204, content={})


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Band Music API",
        "version": "1.0.0",
        "endpoints": {
            "omr": "/api/omr/upload",
            "amt": "/api/amt/upload",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Band Music API"
    }


# ============================================================================
# USE CASE 1: Image/PDF → Playable Music (OMR Pipeline)
# ============================================================================

def update_job_status(job_id: str, status_data: Dict):
    """Update job status in the jobs dictionary."""
    if job_id in jobs:
        jobs[job_id].update(status_data)


async def process_omr_job(job_id: str, upload_path: Path, instrument: str = "piano"):
    """Process OMR job asynchronously."""
    try:
        logger.info(f"Starting OMR processing for job: {job_id} with instrument: {instrument}")
        
        # Run pipeline
        output_path = await omr_pipeline.process(
            upload_path,
            job_id,
            status_callback=update_job_status,
            instrument=instrument
        )
        
        # Update job with success
        jobs[job_id]["output_path"] = str(output_path)
        jobs[job_id]["status"] = "completed"
        logger.info(f"OMR job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"OMR job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/api/omr/upload")
async def upload_image_for_omr(
    file: UploadFile = File(...), 
    background_tasks: BackgroundTasks = None,
    instrument: str = "piano"
):
    """
    Upload an image or PDF for Optical Music Recognition.
    Returns a job ID for tracking the conversion process.
    
    Args:
        file: Music sheet image/PDF file
        instrument: Instrument for synthesis ('piano', 'trombone', 'trumpet')
    """
    try:
        # Validate file type
        allowed_extensions = [".png", ".jpg", ".jpeg", ".pdf"]
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        upload_path = UPLOAD_DIR / f"{job_id}{file_ext}"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize job status
        jobs[job_id] = {
            "type": "omr",
            "status": "uploaded",
            "filename": file.filename,
            "upload_path": str(upload_path),
            "output_path": None,
            "error": None,
            "step": None,
            "progress": 0,
            "instrument": instrument
        }
        
        logger.info(f"OMR job {job_id} created for file: {file.filename} with instrument: {instrument}")
        
        # Start async processing
        background_tasks.add_task(process_omr_job, job_id, upload_path, instrument)
        
        return {
            "job_id": job_id,
            "status": "uploaded",
            "message": "File uploaded successfully. Processing started."
        }
        
    except Exception as e:
        logger.error(f"OMR upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/omr/status/{job_id}")
async def get_omr_status(job_id: str):
    """Get the status of an OMR conversion job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/omr/download/{job_id}")
async def download_omr_result(job_id: str):
    """Download the generated MP3 file."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not complete. Current status: {job['status']}"
        )
    
    output_path = Path(job["output_path"])
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename=f"{job['filename']}.mp3"
    )


# ============================================================================
# USE CASE 2: Audio File → PDF Score (AMT Pipeline)
# ============================================================================

async def process_amt_job(job_id: str, upload_path: Path):
    """Process AMT job asynchronously."""
    try:
        logger.info(f"Starting AMT processing for job: {job_id}")
        
        # Run pipeline
        output_path = await amt_pipeline.process(
            upload_path,
            job_id,
            status_callback=update_job_status
        )
        
        # Update job with success
        jobs[job_id]["output_path"] = str(output_path)
        jobs[job_id]["status"] = "completed"
        logger.info(f"AMT job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"AMT job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/api/amt/upload")
async def upload_audio_for_amt(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Upload an audio file for Automatic Music Transcription.
    Returns a job ID for tracking the conversion process.
    """
    try:
        # Validate file type
        allowed_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".flac"]
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        upload_path = UPLOAD_DIR / f"{job_id}{file_ext}"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize job status
        jobs[job_id] = {
            "type": "amt",
            "status": "uploaded",
            "filename": file.filename,
            "upload_path": str(upload_path),
            "output_path": None,
            "error": None,
            "step": None,
            "progress": 0
        }
        
        logger.info(f"AMT job {job_id} created for file: {file.filename}")
        
        # Start async processing
        background_tasks.add_task(process_amt_job, job_id, upload_path)
        
        return {
            "job_id": job_id,
            "status": "uploaded",
            "message": "File uploaded successfully. Processing started."
        }
        
    except Exception as e:
        logger.error(f"AMT upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/amt/status/{job_id}")
async def get_amt_status(job_id: str):
    """Get the status of an AMT conversion job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/amt/download/{job_id}")
async def download_amt_result(job_id: str):
    """Download the generated PDF score."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not complete. Current status: {job['status']}"
        )
    
    output_path = Path(job["output_path"])
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"{job['filename']}_score.pdf"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
