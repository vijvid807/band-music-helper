"""Music processing utilities using music21."""
from pathlib import Path
from typing import Union
from loguru import logger

from ..config.settings import settings


class MusicConverter:
    """Convert between different music formats using music21."""
    
    def __init__(self):
        """Initialize music converter."""
        logger.info("Initializing music21 converter")
    
    def musicxml_to_midi(self, input_path: Union[str, Path]) -> Path:
        """
        Convert MusicXML to MIDI.
        
        Args:
            input_path: Path to MusicXML file
            
        Returns:
            Path to generated MIDI file
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"MusicXML file not found: {input_path}")
        
        logger.info(f"Converting MusicXML to MIDI: {input_path}")
        
        try:
            from music21 import converter, tempo
            
            # Parse MusicXML
            score = converter.parse(str(input_path))
            
            # Set tempo if not present
            if not score.flatten().getElementsByClass(tempo.MetronomeMark):
                for part in score.parts:
                    part.insert(0, tempo.MetronomeMark(number=120))  # Default 120 BPM
            
            # Write MIDI file
            output_path = settings.output_dir / f"{input_path.stem}.mid"
            score.write('midi', fp=str(output_path))
            
            logger.info(f"MIDI conversion complete: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("music21 library not found. Please install: pip install music21")
            raise RuntimeError("MusicXML to MIDI conversion requires music21 library")
        except Exception as e:
            logger.error(f"MusicXML to MIDI conversion failed: {e}")
            raise RuntimeError(f"Conversion failed: {e}")
    
    def midi_to_musicxml(self, input_path: Union[str, Path]) -> Path:
        """
        Convert MIDI to MusicXML.
        
        Args:
            input_path: Path to MIDI file
            
        Returns:
            Path to generated MusicXML file
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {input_path}")
        
        logger.info(f"Converting MIDI to MusicXML: {input_path}")
        
        try:
            from music21 import converter, instrument
            
            # Parse MIDI file
            score = converter.parse(str(input_path))
            
            # Add instrument information if missing
            for part in score.parts:
                if not part.getElementsByClass(instrument.Instrument):
                    part.insert(0, instrument.Piano())
            
            # Write MusicXML file
            output_path = settings.output_dir / f"{input_path.stem}.musicxml"
            score.write('musicxml', fp=str(output_path))
            
            logger.info(f"MusicXML conversion complete: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("music21 library not found. Please install: pip install music21")
            raise RuntimeError("MIDI to MusicXML conversion requires music21 library")
        except Exception as e:
            logger.error(f"MIDI to MusicXML conversion failed: {e}")
            raise RuntimeError(f"Conversion failed: {e}")
    
    def cleanup(self, file_path: Union[str, Path]):
        """Remove intermediate files if cleanup is enabled."""
        if settings.cleanup_files:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Cleaned up file: {file_path}")
