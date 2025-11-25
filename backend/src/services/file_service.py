"""File service for managing file operations."""
from pathlib import Path
from typing import Optional
import uuid
import shutil
from loguru import logger

from src.config.settings import settings


class FileService:
    """Service for managing file operations."""
    
    def __init__(self):
        """Initialize file service."""
        self.upload_dir = settings.upload_dir
        self.output_dir = settings.output_dir
        logger.info("FileService initialized")
    
    def save_upload(self, file_data, filename: str) -> tuple[str, Path]:
        """
        Save uploaded file and return job ID and file path.
        
        Args:
            file_data: File data stream
            filename: Original filename
            
        Returns:
            Tuple of (job_id, file_path)
        """
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Get file extension
        file_ext = Path(filename).suffix.lower()
        
        # Create upload path
        upload_path = self.upload_dir / f"{job_id}{file_ext}"
        
        # Save file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file_data, buffer)
        
        logger.info(f"Saved upload: {filename} -> {upload_path}")
        return job_id, upload_path
    
    def get_file_path(self, job_id: str, extension: str, directory: str = "output") -> Path:
        """
        Get file path for a job.
        
        Args:
            job_id: Job identifier
            extension: File extension (with dot)
            directory: Directory type ('upload' or 'output')
            
        Returns:
            Path to file
        """
        if directory == "upload":
            return self.upload_dir / f"{job_id}{extension}"
        else:
            return self.output_dir / f"{job_id}{extension}"
    
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists."""
        return file_path.exists()
    
    def delete_file(self, file_path: Path) -> bool:
        """Delete a file."""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Deleted file: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
        return False
    
    def cleanup_job_files(self, job_id: str, extensions: list[str]):
        """
        Clean up all files associated with a job.
        
        Args:
            job_id: Job identifier
            extensions: List of file extensions to clean up
        """
        for ext in extensions:
            # Check upload directory
            upload_file = self.upload_dir / f"{job_id}{ext}"
            self.delete_file(upload_file)
            
            # Check output directory
            output_file = self.output_dir / f"{job_id}{ext}"
            self.delete_file(output_file)
        
        logger.info(f"Cleaned up files for job {job_id}")
    
    def validate_file_extension(self, filename: str, allowed_extensions: list[str]) -> bool:
        """
        Validate file extension.
        
        Args:
            filename: File name
            allowed_extensions: List of allowed extensions (with dots)
            
        Returns:
            True if valid, False otherwise
        """
        file_ext = Path(filename).suffix.lower()
        return file_ext in allowed_extensions
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        if file_path.exists():
            return file_path.stat().st_size
        return 0
