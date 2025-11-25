# Backend Refactoring Guide

## Overview

The backend has been refactored following modern software architecture patterns:

- **Dependency Injection**: Loose coupling between components
- **Service Layer**: Business logic separated from API routes
- **Repository Pattern**: Data access abstraction (prepared for future)
- **Router Composition**: Modular API structure
- **Type Safety**: Pydantic models throughout
- **Async/Await**: Non-blocking operations

## Architecture Layers

### 1. Core Layer (`/src/core/`)

#### `container.py` - Dependency Injection Container
Manages application-wide services and dependencies with lazy loading.

**Pattern**: Singleton with lazy-loaded properties

**Services Managed**:
- Configuration (Settings)
- Processors (OMRProcessor, AMTProcessor)
- Pipelines (OMRPipeline, AMTPipeline)
- Services (JobService, FileService)

**Usage**:
```python
from src.core.container import Container

container = Container()
job_service = container.job_service  # Lazy-loaded on first access
```

#### `dependencies.py` - FastAPI Dependencies
FastAPI dependency functions for automatic injection.

**Available Dependencies**:
- `get_container()`: Returns DI container
- `get_job_service()`: Returns job service
- `get_file_service()`: Returns file service
- `get_omr_pipeline()`: Returns OMR pipeline
- `get_amt_pipeline()`: Returns AMT pipeline

**Usage in Routes**:
```python
@router.post("/upload")
async def upload_file(
    file: UploadFile,
    job_service: JobService = Depends(get_job_service),
    file_service: FileService = Depends(get_file_service),
):
    # Services automatically injected
    pass
```

### 2. Service Layer (`/src/services/`)

#### `job_service.py` - Job Management Service
Handles job lifecycle management.

**Responsibilities**:
- Create jobs with unique IDs
- Update job status and progress
- Retrieve job information
- Track job history

**Key Components**:
```python
class JobType(Enum):
    OMR = "omr"
    AMT = "amt"

class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job:
    job_id: str
    job_type: JobType
    status: JobStatus
    step: Optional[str]
    progress: int
    error: Optional[str]
    created_at: float
    updated_at: float
```

**Methods**:
- `create_job(job_type: JobType) -> Job`
- `get_job(job_id: str) -> Optional[Job]`
- `update_job(job_id: str, **kwargs) -> Job`
- `list_jobs(job_type: Optional[JobType]) -> List[Job]`

#### `file_service.py` - File Operations Service
Handles all file-related operations.

**Responsibilities**:
- Save uploaded files with unique names
- Validate file extensions
- Generate file paths
- Delete files and cleanup
- Manage uploads/outputs directories

**Key Methods**:
- `save_upload(file: UploadFile, job_id: str) -> Path`
- `save_output(content: bytes, job_id: str, extension: str) -> Path`
- `get_output_path(job_id: str, extension: str) -> Path`
- `delete_job_files(job_id: str) -> None`
- `cleanup_old_files(max_age_hours: int) -> int`

### 3. API Layer (`/src/api/`)

#### Router Structure
Modular API with separate routers for each feature.

**Routers**:
- `routes/health.py`: Health check endpoint
- `routes/omr.py`: OMR endpoints (upload, status, download)
- `routes/amt.py`: AMT endpoints (upload, status, download)

**Router Aggregation** (`__init__.py`):
```python
from src.api.routes import health, omr, amt

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(omr.router, prefix="/omr", tags=["omr"])
api_router.include_router(amt.router, prefix="/amt", tags=["amt"])
```

#### Request/Response Models (`/src/api/models/`)

**Separation of Concerns**:
- `requests.py`: Request body models
- `responses.py`: Response models

**Benefits**:
- API contract documentation
- Automatic validation
- Type safety
- OpenAPI schema generation

**Example Models**:
```python
# responses.py
class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    step: Optional[str] = None
    progress: int = 0
    error: Optional[str] = None
    
    class Config:
        from_attributes = True
```

### 4. Processor Layer (`/src/processing/`)

#### Processors
Existing processors (`omr_processor.py`, `amt_processor.py`) integrate with services.

**Updated Pattern**:
```python
class OMRProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
    
    async def process(
        self,
        input_path: Path,
        output_dir: Path,
        callback: Optional[Callable] = None
    ) -> Path:
        if callback:
            await callback(step="preprocessing", progress=10)
        # Process image
        if callback:
            await callback(step="recognition", progress=50)
        # Extract notation
        return output_path
```

#### Pipelines
Orchestrate the complete workflow.

**Pattern**: High-level workflow coordination

**Responsibilities**:
- Coordinate processor steps
- Update job status via service
- Handle errors gracefully
- Manage temporary files

**Example**:
```python
class OMRPipeline:
    def __init__(
        self,
        processor: OMRProcessor,
        job_service: JobService,
        file_service: FileService
    ):
        self.processor = processor
        self.job_service = job_service
        self.file_service = file_service
    
    async def execute(self, job_id: str, input_file: Path) -> Path:
        try:
            self.job_service.update_job(
                job_id,
                status=JobStatus.PROCESSING,
                step="starting"
            )
            
            async def callback(step: str, progress: int):
                self.job_service.update_job(
                    job_id,
                    step=step,
                    progress=progress
                )
            
            output_path = await self.processor.process(
                input_file,
                self.file_service.output_dir,
                callback=callback
            )
            
            self.job_service.update_job(
                job_id,
                status=JobStatus.COMPLETED,
                progress=100
            )
            
            return output_path
            
        except Exception as e:
            self.job_service.update_job(
                job_id,
                status=JobStatus.FAILED,
                error=str(e)
            )
            raise
```

### 5. Main Application (`main_refactored.py`)

#### Modern FastAPI Application

**Key Features**:
- Lifespan events (replaces deprecated startup/shutdown)
- Router composition with API prefix
- CORS middleware configuration
- Dependency injection setup

**Structure**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Band Music Backend")
    container = Container()
    app.state.container = container
    yield
    # Shutdown
    logger.info("Shutting down Band Music Backend")

def create_application() -> FastAPI:
    app = FastAPI(
        title="Band Music API",
        version="2.0.0",
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(CORSMiddleware, ...)
    
    # Routers
    app.include_router(api_router, prefix="/api")
    
    return app

app = create_application()
```

## Benefits of Refactoring

### Before Refactoring
- **Monolithic**: All logic in single main.py file
- **Tight coupling**: Direct dependencies between components
- **Hard to test**: Mocked imports required
- **Code duplication**: Similar logic repeated
- **Limited extensibility**: Adding features required modifying core

### After Refactoring
- **Modular**: Clear separation of concerns
- **Loose coupling**: Dependency injection enables swapping implementations
- **Testable**: Services can be tested in isolation
- **DRY**: Shared logic in service layer
- **Extensible**: New features added via new routers/services

## Usage Patterns

### Adding New Endpoint

1. **Create route file** (`/src/api/routes/new_feature.py`):
```python
from fastapi import APIRouter, Depends
from src.core.dependencies import get_job_service
from src.services.job_service import JobService

router = APIRouter()

@router.post("/new-endpoint")
async def new_endpoint(
    job_service: JobService = Depends(get_job_service)
):
    job = job_service.create_job(JobType.NEW)
    return {"job_id": job.job_id}
```

2. **Register router** (`/src/api/__init__.py`):
```python
from src.api.routes import new_feature

api_router.include_router(
    new_feature.router,
    prefix="/new-feature",
    tags=["new-feature"]
)
```

### Adding New Service

1. **Create service file** (`/src/services/new_service.py`):
```python
from src.config.settings import Settings

class NewService:
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def do_something(self):
        pass
```

2. **Register in container** (`/src/core/container.py`):
```python
@property
def new_service(self) -> NewService:
    if self._new_service is None:
        self._new_service = NewService(self.settings)
    return self._new_service
```

3. **Create dependency** (`/src/core/dependencies.py`):
```python
def get_new_service(
    container: Container = Depends(get_container)
) -> NewService:
    return container.new_service
```

## Testing Strategy

### Unit Tests
Test services in isolation:
```python
def test_job_service_create_job():
    service = JobService()
    job = service.create_job(JobType.OMR)
    
    assert job.job_id is not None
    assert job.status == JobStatus.PENDING
    assert job.progress == 0
```

### Integration Tests
Test API endpoints with dependency overrides:
```python
from fastapi.testclient import TestClient

def test_upload_omr_file():
    client = TestClient(app)
    
    with open("test.png", "rb") as f:
        response = client.post(
            "/api/omr/upload",
            files={"file": ("test.png", f, "image/png")}
        )
    
    assert response.status_code == 200
    assert "job_id" in response.json()
```

### Mock Dependencies
Override dependencies for testing:
```python
from src.core.dependencies import get_job_service

def mock_job_service():
    return MockJobService()

app.dependency_overrides[get_job_service] = mock_job_service
```

## Performance Considerations

1. **Lazy Loading**: Services instantiated only when needed
2. **Singleton Pattern**: Services reused across requests
3. **Async/Await**: Non-blocking I/O operations
4. **Background Tasks**: Heavy processing doesn't block response

## Migration Path

### Phase 1: Parallel Implementation (Current)
- New refactored code in separate files
- Original `main.py` still functional
- Can switch between versions

### Phase 2: Update Processors
- Refactor OMR/AMT processors to use FileService
- Update to async callback pattern
- Remove direct file path logic

### Phase 3: Complete Migration
- Remove old `main.py`
- Rename `main_refactored.py` to `main.py`
- Update documentation

### Phase 4: Add Tests
- Unit tests for all services
- Integration tests for API endpoints
- E2E tests for complete workflows

## Future Enhancements

1. **Database Integration**: Add SQLAlchemy for persistent storage
2. **Celery Integration**: Distributed task processing
3. **Redis Caching**: Cache job statuses and results
4. **WebSocket Support**: Real-time progress updates
5. **Authentication**: Add JWT or OAuth2
6. **Rate Limiting**: Prevent abuse
7. **Metrics**: Prometheus integration for monitoring
8. **API Versioning**: Support multiple API versions

## Configuration

All configuration centralized in `/src/config/settings.py`:

```python
class Settings(BaseSettings):
    # API Config
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Directories
    upload_dir: Path = Path("uploads")
    output_dir: Path = Path("outputs")
    
    # Processing
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: Dict[str, List[str]] = {
        "omr": [".png", ".jpg", ".jpeg", ".pdf"],
        "amt": [".mp3", ".wav", ".ogg", ".m4a"]
    }
    
    class Config:
        env_prefix = "BAND_MUSIC_"
```

## Error Handling

Consistent error handling throughout:

```python
from fastapi import HTTPException, status

# In routes
if not file_service.validate_extension(file.filename, ["omr"]):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invalid file type for OMR"
    )

# In services
try:
    result = await self.processor.process(input_path)
except Exception as e:
    logger.error(f"Processing failed: {e}")
    raise ProcessingError(f"Failed to process file: {e}")
```

## Logging

Structured logging with Loguru:

```python
from loguru import logger

logger.info("Job created", job_id=job_id, type=job_type)
logger.error("Processing failed", job_id=job_id, error=str(e))
```

## API Documentation

Auto-generated docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Summary

The refactored backend provides:
- ✅ Clean architecture with clear separation of concerns
- ✅ Dependency injection for loose coupling
- ✅ Service layer for business logic
- ✅ Modular router structure
- ✅ Type-safe models with Pydantic
- ✅ Extensible design for future features
- ✅ Testable components
- ✅ Modern FastAPI patterns
