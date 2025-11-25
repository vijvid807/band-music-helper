"""Core dependencies for the application."""
from typing import Generator
from src.core.container import get_container, Container


def get_job_service():
    """Dependency for job service."""
    container = get_container()
    return container.job_service


def get_file_service():
    """Dependency for file service."""
    container = get_container()
    return container.file_service


def get_omr_pipeline():
    """Dependency for OMR pipeline."""
    container = get_container()
    return container.omr_pipeline


def get_amt_pipeline():
    """Dependency for AMT pipeline."""
    container = get_container()
    return container.amt_pipeline
