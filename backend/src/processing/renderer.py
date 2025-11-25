"""Score rendering utilities using LilyPond."""
from pathlib import Path
from typing import Union
from loguru import logger
from music21 import converter, stream, lily

from ..config.settings import settings


class ScoreRenderer:
    """Render musical scores to PDF using LilyPond."""
    
    def __init__(self):
        """Initialize score renderer."""
        logger.info("Initializing LilyPond score renderer")
    
    def midi_to_pdf(self, input_path: Union[str, Path]) -> Path:
        """
        Render MIDI to PDF using LilyPond directly.
        
        Args:
            input_path: Path to MIDI file
            
        Returns:
            Path to generated PDF file
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {input_path}")
        
        logger.info(f"Rendering MIDI to PDF: {input_path}")
        
        try:
            import subprocess
            import shutil
            
            # Check if LilyPond is available
            if not shutil.which('lilypond'):
                raise RuntimeError("LilyPond not found. Please install LilyPond: https://lilypond.org/")
            
            # Check if midi2ly is available (comes with LilyPond)
            if not shutil.which('midi2ly'):
                raise RuntimeError("midi2ly not found. Please install LilyPond: https://lilypond.org/")
            
            # Convert MIDI to LilyPond format using midi2ly
            ly_path = settings.output_dir / f"{input_path.stem}.ly"
            
            logger.info(f"Converting MIDI to LilyPond: {input_path}")
            midi2ly_cmd = [
                'midi2ly',
                '--duration-quant=16',  # Quantize durations to 16th notes
                '--key=0:0',            # Default key signature (C major: 0 sharps/flats, major mode)
                f'--output={ly_path}',
                str(input_path)
            ]
            
            result = subprocess.run(
                midi2ly_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.error(f"midi2ly error: {result.stderr}")
                raise RuntimeError(f"MIDI to LilyPond conversion failed: {result.stderr}")
            
            # Post-process the LilyPond file to add formatting directives
            with open(ly_path, 'r', encoding='utf-8') as f:
                ly_content = f.read()
            
            # Add better formatting settings before the \score block
            formatting_header = r'''
\paper {
  #(set-paper-size "letter")
  indent = 0\mm
  line-width = 180\mm
  ragged-right = ##f
  ragged-last = ##f
  ragged-bottom = ##f
  system-system-spacing = #'((basic-distance . 12) (minimum-distance . 8) (padding . 1))
}

\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
}

'''
            
            # Insert before \score block
            if '\\score' in ly_content:
                ly_content = ly_content.replace('\\score', formatting_header + '\\score', 1)
            else:
                # Fallback: add at the end
                ly_content = ly_content + '\n' + formatting_header
            
            with open(ly_path, 'w', encoding='utf-8') as f:
                f.write(ly_content)
            
            # Render PDF using LilyPond
            logger.info(f"Rendering PDF from LilyPond file: {ly_path}")
            pdf_path = settings.output_dir / f"{input_path.stem}.pdf"
            
            lily_cmd = [
                'lilypond',
                '--pdf',
                f'--output={input_path.stem}',
                str(ly_path)
            ]
            
            result = subprocess.run(
                lily_cmd,
                cwd=settings.output_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stderr:
                logger.warning(f"LilyPond warning: {result.stderr}")
            
            if not pdf_path.exists():
                raise RuntimeError(f"PDF was not created. LilyPond output: {result.stderr}")
            
            logger.info(f"PDF rendering complete: {pdf_path}")
            return pdf_path
            
        except subprocess.TimeoutExpired:
            logger.error("LilyPond rendering timed out")
            raise RuntimeError("PDF rendering timed out")
        except Exception as e:
            logger.error(f"Error rendering PDF: {str(e)}")
            raise
    
    def musicxml_to_pdf(self, input_path: Union[str, Path]) -> Path:
        """
        Render MusicXML to PDF using LilyPond.
        
        Args:
            input_path: Path to MusicXML file
            
        Returns:
            Path to generated PDF file
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"MusicXML file not found: {input_path}")
        
        logger.info(f"Rendering score to PDF: {input_path}")
        
        try:
            # Try using music21 with LilyPond
            try:
                import subprocess
                import shutil
                
                # Check if LilyPond is available
                if not shutil.which('lilypond'):
                    raise RuntimeError("LilyPond not found. Please install LilyPond: https://lilypond.org/")
                
                # Parse MusicXML
                score = converter.parse(str(input_path))
                
                # Flatten polyphonic parts into a single staff with chords
                # This prevents the complex multi-voice structures that cause poor layout
                flat_score = stream.Score()
                flat_part = stream.Part()
                
                # Group notes by offset (time) to create chords
                notes_by_offset = {}
                for element in score.flatten().notesAndRests:
                    offset = element.offset
                    if offset not in notes_by_offset:
                        notes_by_offset[offset] = []
                    notes_by_offset[offset].append(element)
                
                # Create simplified score with chords where multiple notes occur
                from music21 import note, chord as m21_chord
                for offset in sorted(notes_by_offset.keys()):
                    elements = notes_by_offset[offset]
                    
                    # Filter out rests if there are notes
                    notes_only = [e for e in elements if isinstance(e, note.Note)]
                    rests_only = [e for e in elements if isinstance(e, note.Rest)]
                    
                    if notes_only:
                        if len(notes_only) == 1:
                            flat_part.insert(offset, notes_only[0])
                        else:
                            # Create chord from multiple notes
                            pitches = [n.pitch for n in notes_only]
                            duration = notes_only[0].duration
                            new_chord = m21_chord.Chord(pitches, duration=duration)
                            flat_part.insert(offset, new_chord)
                    elif rests_only:
                        flat_part.insert(offset, rests_only[0])
                
                # Add to score
                flat_score.append(flat_part)
                
                # Write as LilyPond format
                ly_path = settings.output_dir / f"{input_path.stem}.ly"
                flat_score.write('lilypond', fp=str(ly_path))
                
                # Post-process the LilyPond file to add formatting directives
                with open(ly_path, 'r', encoding='utf-8') as f:
                    ly_content = f.read()
                
                # Add better formatting settings
                formatting_header = r'''
\paper {
  #(set-paper-size "letter")
  indent = 0\mm
  line-width = 180\mm
  ragged-right = ##f
  ragged-last = ##f
  ragged-bottom = ##f
  system-system-spacing = #'((basic-distance . 12) (minimum-distance . 8) (padding . 1))
}

\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
}
'''
                
                # Insert after \version line
                if '\\version' in ly_content:
                    parts = ly_content.split('\\version', 1)
                    if len(parts) == 2:
                        version_end = parts[1].find('\n')
                        ly_content = parts[0] + '\\version' + parts[1][:version_end+1] + formatting_header + parts[1][version_end+1:]
                else:
                    ly_content = formatting_header + ly_content
                
                with open(ly_path, 'w', encoding='utf-8') as f:
                    f.write(ly_content)
                
                # Render with LilyPond
                output_path = settings.output_dir / f"{input_path.stem}.pdf"
                cmd = [
                    'lilypond',
                    '--pdf',
                    f'--output={input_path.stem}',
                    str(ly_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    cwd=str(settings.output_dir),
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    logger.warning(f"LilyPond warning: {result.stderr}")
                
                # Clean up intermediate files
                if settings.cleanup_files:
                    ly_path.unlink(missing_ok=True)
                    # LilyPond creates additional files
                    for ext in ['.log', '.ps']:
                        temp_file = settings.output_dir / f"{input_path.stem}{ext}"
                        temp_file.unlink(missing_ok=True)
                
                if not output_path.exists():
                    raise FileNotFoundError("PDF was not generated by LilyPond")
                
                logger.info(f"PDF rendering complete: {output_path}")
                return output_path
                
            except ImportError:
                logger.error("music21 library not found. Please install: pip install music21")
                raise RuntimeError("PDF rendering requires music21 library")
            
        except Exception as e:
            logger.error(f"PDF rendering failed: {e}")
            raise RuntimeError(f"Rendering failed: {e}")
    
    def cleanup(self, file_path: Union[str, Path]):
        """Remove intermediate files if cleanup is enabled."""
        if settings.cleanup_files:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Cleaned up file: {file_path}")
