"""Dependency injection container for the application."""
from functools import lru_cache
from typing import Optional

from src.omr.processor import OMRProcessor
from src.amt.processor import AMTProcessor
from src.processing.converter import MusicConverter
from src.processing.synthesizer import AudioSynthesizer
from src.processing.renderer import ScoreRenderer
from src.pipeline.omr_pipeline import OMRPipeline
from src.pipeline.amt_pipeline import AMTPipeline
from src.services.job_service import JobService
from src.services.file_service import FileService
from src.config.settings import settings


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._omr_processor: Optional[OMRProcessor] = None
        self._amt_processor: Optional[AMTProcessor] = None
        self._music_converter: Optional[MusicConverter] = None
        self._audio_synthesizer: Optional[AudioSynthesizer] = None
        self._score_renderer: Optional[ScoreRenderer] = None
        self._omr_pipeline: Optional[OMRPipeline] = None
        self._amt_pipeline: Optional[AMTPipeline] = None
        self._job_service: Optional[JobService] = None
        self._file_service: Optional[FileService] = None
    
    @property
    def omr_processor(self) -> OMRProcessor:
        if self._omr_processor is None:
            self._omr_processor = OMRProcessor()
        return self._omr_processor
    
    @property
    def amt_processor(self) -> AMTProcessor:
        if self._amt_processor is None:
            self._amt_processor = AMTProcessor()
        return self._amt_processor
    
    @property
    def music_converter(self) -> MusicConverter:
        if self._music_converter is None:
            self._music_converter = MusicConverter()
        return self._music_converter
    
    @property
    def audio_synthesizer(self) -> AudioSynthesizer:
        if self._audio_synthesizer is None:
            self._audio_synthesizer = AudioSynthesizer()
        return self._audio_synthesizer
    
    @property
    def score_renderer(self) -> ScoreRenderer:
        if self._score_renderer is None:
            self._score_renderer = ScoreRenderer()
        return self._score_renderer
    
    @property
    def omr_pipeline(self) -> OMRPipeline:
        if self._omr_pipeline is None:
            self._omr_pipeline = OMRPipeline()
        return self._omr_pipeline
    
    @property
    def amt_pipeline(self) -> AMTPipeline:
        if self._amt_pipeline is None:
            self._amt_pipeline = AMTPipeline()
        return self._amt_pipeline
    
    @property
    def job_service(self) -> JobService:
        if self._job_service is None:
            self._job_service = JobService()
        return self._job_service
    
    @property
    def file_service(self) -> FileService:
        if self._file_service is None:
            self._file_service = FileService()
        return self._file_service


@lru_cache()
def get_container() -> Container:
    """Get singleton container instance."""
    return Container()
