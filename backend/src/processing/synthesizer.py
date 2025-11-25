"""Audio synthesis utilities."""
from pathlib import Path
from typing import Union
from loguru import logger

from ..config.settings import settings


class AudioSynthesizer:
    """Synthesize audio from MIDI files."""
    
    # MIDI Program numbers for General MIDI instruments
    INSTRUMENTS = {
        "piano": 0,      # Acoustic Grand Piano
        "trombone": 57,  # Trombone
        "trumpet": 56    # Trumpet
    }
    
    def __init__(self):
        """Initialize audio synthesizer."""
        self.soundfont = settings.fluidsynth_soundfont
        self.sample_rate = settings.fluidsynth_sample_rate
        logger.info(f"Initializing audio synthesizer with soundfont: {self.soundfont}")
    
    def midi_to_audio(self, input_path: Union[str, Path], output_format: str = "mp3", instrument: str = "piano") -> Path:
        """
        Convert MIDI to audio (MP3/WAV).
        
        Args:
            input_path: Path to MIDI file
            output_format: Output format ('mp3' or 'wav')
            instrument: Instrument name ('piano', 'trombone', 'trumpet')
            
        Returns:
            Path to generated audio file
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {input_path}")
        
        # Validate instrument
        instrument = instrument.lower()
        if instrument not in self.INSTRUMENTS:
            logger.warning(f"Unknown instrument '{instrument}', defaulting to piano")
            instrument = "piano"
        
        logger.info(f"Synthesizing audio from MIDI: {input_path} (instrument: {instrument})")
        
        # Apply instrument change to MIDI file
        modified_midi_path = self._apply_instrument_change(input_path, instrument)
        
        try:
            import subprocess
            
            # Create WAV first using FluidSynth command line
            wav_path = settings.output_dir / f"{input_path.stem}.wav"
            
            # Call FluidSynth directly (more reliable than midi2audio wrapper)
            # Correct syntax: options first, then soundfont, then MIDI file
            cmd = [
                "fluidsynth",
                "-ni",  # non-interactive mode
                "-F", str(wav_path),  # output file
                "-T", "wav",  # file type
                "-O", "s16",  # 16-bit signed PCM
                "-r", str(self.sample_rate),  # sample rate
                str(self.soundfont),  # soundfont after options
                str(modified_midi_path)  # Use modified MIDI with instrument change
            ]
            
            logger.debug(f"Running FluidSynth: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Log output for debugging
            if result.stdout:
                logger.debug(f"FluidSynth stdout: {result.stdout}")
            if result.stderr:
                logger.debug(f"FluidSynth stderr: {result.stderr}")
            
            if result.returncode != 0:
                raise RuntimeError(f"FluidSynth failed with code {result.returncode}: {result.stderr}")
            
            if not wav_path.exists():
                raise FileNotFoundError(f"FluidSynth did not create output file: {wav_path}")
            
            # Convert to MP3 if requested
            if output_format.lower() == "mp3":
                from pydub import AudioSegment
                output_path = settings.output_dir / f"{input_path.stem}.mp3"
                audio = AudioSegment.from_wav(str(wav_path))
                audio.export(str(output_path), format="mp3", bitrate="192k")
                if settings.cleanup_files:
                    wav_path.unlink()  # Remove intermediate WAV
            else:
                output_path = wav_path
            
            logger.info(f"Audio synthesis complete: {output_path} (instrument: {instrument})")
            
            # Cleanup modified MIDI if it was created
            if modified_midi_path != input_path:
                modified_midi_path.unlink(missing_ok=True)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Audio synthesis failed: {e}")
            raise RuntimeError(f"Synthesis failed: {e}")
    
    def _apply_instrument_change(self, midi_path: Path, instrument: str) -> Path:
        """Apply instrument program change to all tracks in MIDI file."""
        try:
            import mido
            
            # Read MIDI file
            midi = mido.MidiFile(str(midi_path))
            program_number = self.INSTRUMENTS[instrument]
            
            # Create new MIDI with instrument changes
            modified_midi = mido.MidiFile(ticks_per_beat=midi.ticks_per_beat)
            
            for track in midi.tracks:
                new_track = mido.MidiTrack()
                
                # Add program change at the start for all channels
                program_added = False
                
                # Copy all messages, but filter out existing program_change messages
                for msg in track:
                    # Skip existing program_change messages (we'll add our own)
                    if msg.type == 'program_change':
                        continue
                    
                    # Add our program change before the first note_on
                    if not program_added and msg.type == 'note_on':
                        # Add program change for all 16 MIDI channels
                        for channel in range(16):
                            if channel != 9:  # Skip channel 10 (drums)
                                new_track.append(mido.Message('program_change', 
                                                             program=program_number, 
                                                             channel=channel, 
                                                             time=0))
                        program_added = True
                    
                    # Copy the message
                    new_track.append(msg)
                
                modified_midi.tracks.append(new_track)
            
            # Save modified MIDI
            modified_path = settings.output_dir / f"{midi_path.stem}_instrument.mid"
            modified_midi.save(str(modified_path))
            
            logger.debug(f"Applied instrument change: {instrument} (program {program_number})")
            return modified_path
            
        except ImportError:
            logger.warning("mido library not available, skipping instrument change")
            return midi_path
        except Exception as e:
            logger.warning(f"Failed to apply instrument change: {e}, using original MIDI")
            return midi_path
    
    def cleanup(self, file_path: Union[str, Path]):
        """Remove intermediate files if cleanup is enabled."""
        if settings.cleanup_files:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Cleaned up file: {file_path}")
