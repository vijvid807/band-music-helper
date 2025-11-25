"""AMT Pipeline: Audio → MIDI → MusicXML → PDF."""
from pathlib import Path
from typing import Dict, Callable
from loguru import logger

from ..amt.processor import AMTProcessor
from ..processing.converter import MusicConverter
from ..processing.renderer import ScoreRenderer


class AMTPipeline:
    """Complete pipeline for AMT processing."""
    
    def __init__(self):
        """Initialize pipeline components."""
        self.amt = AMTProcessor()
        self.converter = MusicConverter()
        self.renderer = ScoreRenderer()
    
    async def process(
        self,
        input_path: Path,
        job_id: str,
        status_callback: Callable[[str, Dict], None] = None
    ) -> Path:
        """
        Process audio through AMT pipeline to PDF score.
        
        Args:
            input_path: Path to input audio file
            job_id: Unique job identifier
            status_callback: Optional callback for status updates
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Step 1: AMT - Audio → MIDI
            if status_callback:
                status_callback(job_id, {"status": "processing", "step": "transcription", "progress": 25})
            
            logger.info(f"[{job_id}] Starting AMT processing")
            midi_path = self.amt.process_audio(input_path)
            logger.info(f"[{job_id}] AMT complete: {midi_path}")
            
            # Step 2: Render MIDI → PDF directly (bypassing MusicXML to avoid formatting issues)
            if status_callback:
                status_callback(job_id, {"status": "processing", "step": "rendering", "progress": 75})
            
            logger.info(f"[{job_id}] Rendering PDF from MIDI")
            pdf_path = self.renderer.midi_to_pdf(midi_path)
            logger.info(f"[{job_id}] PDF rendering complete: {pdf_path}")
            
            # Cleanup intermediate files
            self.amt.cleanup(midi_path)
            
            if status_callback:
                status_callback(job_id, {"status": "completed", "progress": 100})
            
            logger.info(f"[{job_id}] Pipeline complete: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"[{job_id}] Pipeline failed: {e}")
            if status_callback:
                status_callback(job_id, {"status": "failed", "error": str(e)})
            raise
