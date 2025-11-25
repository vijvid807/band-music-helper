"""OMR Pipeline: Image/PDF → MusicXML → MIDI → Audio."""
from pathlib import Path
from typing import Dict, Callable
from loguru import logger

from ..omr.processor import OMRProcessor
from ..processing.converter import MusicConverter
from ..processing.synthesizer import AudioSynthesizer


class OMRPipeline:
    """Complete pipeline for OMR processing."""
    
    def __init__(self):
        """Initialize pipeline components."""
        self.omr = OMRProcessor()
        self.converter = MusicConverter()
        self.synthesizer = AudioSynthesizer()
    
    async def process(
        self,
        input_path: Path,
        job_id: str,
        status_callback: Callable[[str, Dict], None] = None,
        instrument: str = "piano"
    ) -> Path:
        """
        Process image/PDF through OMR pipeline to audio.
        
        Args:
            input_path: Path to input image/PDF
            job_id: Unique job identifier
            status_callback: Optional callback for status updates
            instrument: Instrument for audio synthesis ('piano', 'trombone', 'trumpet')
            
        Returns:
            Path to generated audio file
        """
        try:
            # Step 1: OMR - Image/PDF → MusicXML
            if status_callback:
                status_callback(job_id, {"status": "processing", "step": "omr", "progress": 25})
            
            logger.info(f"[{job_id}] Starting OMR processing")
            musicxml_path = self.omr.process_image(input_path)
            logger.info(f"[{job_id}] OMR complete: {musicxml_path}")
            
            # Step 2: Convert MusicXML → MIDI
            if status_callback:
                status_callback(job_id, {"status": "processing", "step": "conversion", "progress": 50})
            
            logger.info(f"[{job_id}] Converting to MIDI")
            midi_path = self.converter.musicxml_to_midi(musicxml_path)
            logger.info(f"[{job_id}] MIDI conversion complete: {midi_path}")
            
            # Step 3: Synthesize MIDI → Audio
            if status_callback:
                status_callback(job_id, {"status": "processing", "step": "synthesis", "progress": 75})
            
            logger.info(f"[{job_id}] Synthesizing audio with instrument: {instrument}")
            audio_path = self.synthesizer.midi_to_audio(midi_path, output_format="mp3", instrument=instrument)
            logger.info(f"[{job_id}] Audio synthesis complete: {audio_path}")
            
            # Cleanup intermediate files
            self.omr.cleanup(musicxml_path)
            self.converter.cleanup(midi_path)
            
            if status_callback:
                status_callback(job_id, {"status": "completed", "progress": 100})
            
            logger.info(f"[{job_id}] Pipeline complete: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"[{job_id}] Pipeline failed: {e}")
            if status_callback:
                status_callback(job_id, {"status": "failed", "error": str(e)})
            raise
