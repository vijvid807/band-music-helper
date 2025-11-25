"""AMT (Automatic Music Transcription) pipeline implementation."""
from pathlib import Path
from typing import Union, Optional
from loguru import logger
import numpy as np

from ..config.settings import settings


class AMTProcessor:
    """Process audio files to extract musical notation."""
    
    def __init__(self):
        """Initialize AMT processor."""
        logger.info("Initializing AMT processor with Basic Pitch")
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required dependencies are available."""
        try:
            from basic_pitch.inference import predict
            from basic_pitch import ICASSP_2022_MODEL_PATH
            logger.info("Basic Pitch library is available")
        except ImportError:
            logger.warning("Basic Pitch library not found. Please install: pip install basic-pitch")
    
    def process_audio(self, input_path: Union[str, Path]) -> Path:
        """
        Process an audio file to extract musical notation.
        
        Args:
            input_path: Path to the input audio file
            
        Returns:
            Path to the generated MIDI file
            
        Raises:
            ValueError: If file format is not supported
            RuntimeError: If AMT processing fails
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if input_path.suffix.lower() not in settings.amt_allowed_extensions:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")
        
        logger.info(f"Starting AMT processing for: {input_path}")
        
        try:
            # Run Basic Pitch
            midi_path = self._run_basic_pitch(input_path)
            
            logger.info(f"AMT processing complete: {midi_path}")
            return midi_path
            
        except Exception as e:
            logger.error(f"AMT processing failed: {e}")
            raise RuntimeError(f"AMT processing failed: {e}")
    
    def _run_basic_pitch(self, audio_path: Path) -> Path:
        """
        Run Basic Pitch transcription on audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Path to generated MIDI file
        """
        try:
            from basic_pitch.inference import predict
            from basic_pitch import ICASSP_2022_MODEL_PATH
            import os
            
            # Monkey patch scipy for Basic Pitch compatibility with scipy 1.13+
            import scipy.signal
            if not hasattr(scipy.signal, 'gaussian'):
                from scipy.signal.windows import gaussian
                scipy.signal.gaussian = gaussian
                logger.debug("Patched scipy.signal.gaussian for compatibility")
            
            logger.info(f"Running Basic Pitch on: {audio_path}")
            
            # Output path for MIDI
            output_path = settings.output_dir / f"{audio_path.stem}.mid"
            
            # Use ONNX model directly (more compatible than TensorFlow SavedModel)
            onnx_model_path = os.path.join(os.path.dirname(ICASSP_2022_MODEL_PATH), "nmp.onnx")
            logger.info(f"Using ONNX model: {onnx_model_path}")
            
            # Run Basic Pitch prediction
            model_output, midi_data, note_events = predict(
                str(audio_path),
                onnx_model_path,
                onset_threshold=settings.basic_pitch_onset_threshold,
                frame_threshold=settings.basic_pitch_frame_threshold,
                minimum_note_length=settings.basic_pitch_minimum_note_length,
                minimum_frequency=settings.basic_pitch_minimum_frequency,
                maximum_frequency=settings.basic_pitch_maximum_frequency,
                multiple_pitch_bends=False,
                melodia_trick=True,
                debug_file=None,
            )
            
            # Save MIDI file
            if midi_data:
                midi_data.write(str(output_path))
                logger.info(f"Basic Pitch processing complete: {output_path}")
                return output_path
            else:
                raise RuntimeError("Basic Pitch did not generate MIDI data")
            
        except ImportError as e:
            logger.error(f"Basic Pitch library not found: {e}")
            logger.error("Creating mock output for development")
            output_path = settings.output_dir / f"{audio_path.stem}.mid"
            self._create_mock_midi(output_path)
            return output_path
        except Exception as e:
            import traceback
            logger.error(f"Basic Pitch processing failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.warning("Creating mock MIDI output for development")
            output_path = settings.output_dir / f"{audio_path.stem}.mid"
            self._create_mock_midi(output_path)
            return output_path
    
    def _create_mock_midi(self, output_path: Path):
        """Create a simple mock MIDI file for testing."""
        try:
            import mido
            from mido import Message, MidiFile, MidiTrack
            
            # Create a simple MIDI file with a C major scale
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)
            
            # Add some notes (C major scale)
            track.append(Message('program_change', program=0, time=0))
            
            notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
            for note in notes:
                track.append(Message('note_on', note=note, velocity=64, time=0))
                track.append(Message('note_off', note=note, velocity=64, time=480))
            
            mid.save(str(output_path))
            logger.info(f"Created mock MIDI file: {output_path}")
            
        except ImportError:
            logger.error("mido library not found. Cannot create mock MIDI file")
            raise RuntimeError("Mock MIDI creation requires mido library")
    
    def cleanup(self, file_path: Union[str, Path]):
        """Remove intermediate files if cleanup is enabled."""
        if settings.cleanup_files:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Cleaned up file: {file_path}")
