"""Configuration settings for Band Music API."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""
    
    # App metadata
    app_name: str = "Band Music API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Directory paths
    base_dir: Path = Path(__file__).parent.parent.parent  # Go up to /backend/ directory
    upload_dir: Path = base_dir / "uploads"
    output_dir: Path = base_dir / "outputs"
    logs_dir: Path = base_dir / "logs"
    
    # File size limits (in bytes)
    max_upload_size_mb: int = 100
    max_upload_size: int = max_upload_size_mb * 1024 * 1024
    
    # Supported file formats
    omr_allowed_extensions: list[str] = [".png", ".jpg", ".jpeg", ".pdf"]
    amt_allowed_extensions: list[str] = [".mp3", ".wav", ".ogg", ".m4a"]
    
    # OMR Settings (Oemer)
    oemer_model_path: str = "BobvanHoed/oemer-small"
    
    # AMT Settings (Basic Pitch)
    basic_pitch_onset_threshold: float = 0.5
    basic_pitch_frame_threshold: float = 0.3
    basic_pitch_minimum_note_length: int = 127
    basic_pitch_minimum_frequency: float = 65.41  # C2 (lowest note on cello/bass)
    basic_pitch_maximum_frequency: float = 2093.0  # C7 (very high piano note)
    basic_pitch_multiple_pitch_bends: bool = False
    
    # Music21 Settings
    music21_midi_program: int = 0  # Acoustic Grand Piano
    music21_tempo_bpm: int = 120
    
    # FluidSynth Settings
    fluidsynth_soundfont: str = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
    fluidsynth_sample_rate: int = 44100
    
    # LilyPond Settings
    lilypond_format: str = "pdf"
    lilypond_resolution: int = 300
    
    # Processing settings
    cleanup_files: bool = True  # Delete intermediate files after processing
    job_timeout_seconds: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
settings = Settings()

# Ensure directories exist
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.logs_dir.mkdir(parents=True, exist_ok=True)
