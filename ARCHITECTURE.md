# Band Music - Project Architecture

## Overview

Band Music is a full-stack web application that enables bidirectional conversion between sheet music and audio using state-of-the-art AI and open-source music libraries.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  OMRConverter    │              │  AMTConverter    │        │
│  │  Component       │              │  Component       │        │
│  └────────┬─────────┘              └────────┬─────────┘        │
│           │                                  │                  │
│           └──────────┬──────────────────────┘                  │
│                      │                                          │
│                 ┌────▼─────┐                                   │
│                 │  API      │                                   │
│                 │  Service  │                                   │
│                 └────┬─────┘                                   │
└──────────────────────┼──────────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────────┐
│                    Backend (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     main.py                               │  │
│  │  - File upload endpoints                                  │  │
│  │  - Job status tracking                                    │  │
│  │  - Result download                                        │  │
│  │  - Background task processing                             │  │
│  └────────────────┬──────────────────────────┬───────────────┘  │
│                   │                          │                  │
│      ┌────────────▼─────────┐    ┌──────────▼──────────┐      │
│      │   OMR Pipeline       │    │   AMT Pipeline       │      │
│      └────────────┬─────────┘    └──────────┬──────────┘      │
│                   │                          │                  │
│  ┌────────────────▼───────────┐  ┌──────────▼─────────────┐   │
│  │  OMR Processor (Oemer)     │  │  AMT Processor          │   │
│  │  - Image/PDF to MusicXML   │  │  (Basic Pitch)          │   │
│  └────────────┬───────────────┘  │  - Audio to MIDI        │   │
│               │                  └──────────┬─────────────┘   │
│               │                             │                  │
│  ┌────────────▼─────────────────────────────▼─────────────┐   │
│  │          Music Converter (music21)                      │   │
│  │  - MusicXML ↔ MIDI conversion                          │   │
│  │  - Score manipulation                                   │   │
│  └────────────┬─────────────────────────────┬─────────────┘   │
│               │                             │                  │
│  ┌────────────▼─────────┐     ┌────────────▼─────────────┐   │
│  │  Audio Synthesizer   │     │  Score Renderer          │   │
│  │  (FluidSynth)        │     │  (LilyPond)              │   │
│  │  - MIDI to MP3       │     │  - MusicXML to PDF       │   │
│  └──────────────────────┘     └──────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Components

#### 1. App.tsx
- Main application container
- Tab navigation between OMR and AMT converters
- Layout and styling

#### 2. OMRConverter.tsx
- Sheet music upload interface
- Real-time progress tracking
- MP3 download functionality
- Pipeline visualization

#### 3. AMTConverter.tsx
- Audio file upload interface
- Status monitoring
- PDF score download
- Process step indicators

#### 4. API Service (api.ts)
- Axios-based HTTP client
- API endpoint abstractions
- Type-safe interfaces
- Error handling

### Backend Components

#### 1. FastAPI Application (main.py)
**Responsibilities:**
- HTTP endpoint management
- File upload handling
- Job queue management
- Background task orchestration
- CORS configuration

**Key Endpoints:**
- `POST /api/omr/upload` - Upload sheet music
- `GET /api/omr/status/{id}` - Check conversion status
- `GET /api/omr/download/{id}` - Download audio
- `POST /api/amt/upload` - Upload audio file
- `GET /api/amt/status/{id}` - Check transcription status
- `GET /api/amt/download/{id}` - Download PDF score

#### 2. OMR Pipeline (omr_pipeline.py)
**Processing Steps:**
1. Image/PDF validation
2. OMR processing (Oemer)
3. MusicXML to MIDI conversion (music21)
4. Instrument program change injection (mido)
5. MIDI to MP3 synthesis (FluidSynth)
6. Cleanup intermediate files

**Supported Instruments:**
- Piano (GM Program 0) - Default
- Trombone (GM Program 57)
- Trumpet (GM Program 56)

**Status Callbacks:**
- Upload complete (0%)
- OMR processing (25%)
- MIDI conversion (50%)
- Audio synthesis (75%)
- Complete (100%)

#### 3. AMT Pipeline (amt_pipeline.py)
**Processing Steps:**
1. Audio file validation
2. Audio transcription (Basic Pitch)
3. MIDI to MusicXML conversion (music21)
4. PDF score rendering (LilyPond)
5. Cleanup intermediate files

**Status Callbacks:**
- Upload complete (0%)
- Transcription (25%)
- MusicXML conversion (50%)
- PDF rendering (75%)
- Complete (100%)

#### 4. OMR Processor (omr/processor.py)
**Technology:** Oemer (Open-source OMR)

**Features:**
- Multi-format support (PNG, JPG, PDF)
- PDF to image conversion
- Symbol detection
- Staff recognition
- MusicXML generation
- Fallback mock data for development

**Limitations:**
- Works best with 1-2 staff music
- Complex multi-staff scores (3+ staves) may fail
- Single melody lines recommended (solos, simple pieces)
- Higher quality images produce better results

**Error Handling:**
- Detects assertion errors for complex music
- Provides clear error messages with suggestions
- Recommends using simpler sheet music or cropping to single staff

#### 5. AMT Processor (amt/processor.py)
**Technology:** Basic Pitch (Spotify)

**Features:**
- Multi-format audio support
- Pitch detection
- Rhythm analysis
- Polyphonic transcription
- MIDI file generation
- Configurable thresholds

#### 6. Music Converter (processing/converter.py)
**Technology:** music21

**Capabilities:**
- MusicXML parsing
- MIDI file I/O
- Tempo manipulation
- Instrument assignment
- Score validation
- Format conversion

#### 7. Audio Synthesizer (processing/synthesizer.py)
**Technology:** FluidSynth + midi2audio + mido

**Features:**
- High-quality synthesis
- Configurable soundfonts
- Instrument selection (Piano, Trombone, Trumpet)
- MIDI program change injection
- Removes existing program changes to ensure correct instrument
- Sample rate control
- MP3/WAV output
- Batch processing support

**Instrument Implementation:**
- Uses General MIDI standard program numbers
- Strips existing program_change messages from MIDI files
- Injects selected instrument program across all non-drum channels
- Applied before FluidSynth synthesis for accurate sound

#### 8. Score Renderer (processing/renderer.py)
**Technology:** LilyPond

**Features:**
- Professional typesetting
- PDF generation
- MusicXML input
- High-resolution output
- Layout optimization

## Data Flow

### OMR Pipeline Flow
```
User Upload + Instrument Selection → FastAPI → Save File → Job Created
                ↓
         Background Task
                ↓
    ┌───────────────────────┐
    │  OMR Pipeline         │
    ├───────────────────────┤
    │ 1. Load Image/PDF     │
    │ 2. Run Oemer          │
    │    → MusicXML         │
    │ 3. Parse with music21 │
    │    → MIDI             │
    │ 4. Inject Instrument  │
    │    (mido)             │
    │ 5. Synthesize         │
    │    → MP3              │
    └───────────────────────┘
                ↓
    Update Job Status → User Downloads MP3 (with selected instrument)
```

### AMT Pipeline Flow
```
User Upload → FastAPI → Save File → Job Created
                ↓
         Background Task
                ↓
    ┌───────────────────────┐
    │  AMT Pipeline         │
    ├───────────────────────┤
    │ 1. Load Audio         │
    │ 2. Run Basic Pitch    │
    │    → MIDI             │
    │ 3. Parse with music21 │
    │    → MusicXML         │
    │ 4. Render LilyPond    │
    │    → PDF              │
    └───────────────────────┘
                ↓
    Update Job Status → User Downloads PDF
```

## File Format Pipeline

### Use Case 1: Sheet Music → Audio
```
PNG/JPG/PDF → MusicXML → MIDI → MIDI+Instrument → WAV → MP3
    ↑            ↑         ↑           ↑            ↑      ↑
  Oemer       music21   music21      mido          FS   pydub
                                   (strip old,
                                   add program
                                    change)
```

### Use Case 2: Audio → Sheet Music
```
MP3/WAV → MIDI → MusicXML → LilyPond → PDF
    ↑       ↑        ↑           ↑        ↑
Basic Pitch    music21      music21   LilyPond
```

## State Management

### Job Status States
1. **uploaded** - File received, queued for processing
2. **processing** - Active conversion in progress
3. **completed** - Successfully finished
4. **failed** - Error occurred during processing

### Job Object Structure
```typescript
{
  job_id: string,
  type: 'omr' | 'amt',
  status: 'uploaded' | 'processing' | 'completed' | 'failed',
  filename: string,
  upload_path: string,
  output_path: string | null,
  error: string | null,
  step: string | null,  // Current processing step
  progress: number      // 0-100
}
```

## Error Handling

### Frontend
- File validation before upload
- Network error handling
- Status polling with timeout
- User-friendly error messages

### Backend
- Input validation with Pydantic
- Try-catch blocks in pipelines
- Detailed error logging
- Graceful degradation (mock outputs for dev)

## Performance Considerations

### Backend Optimization
- Async/await for I/O operations
- Background task processing
- Efficient file cleanup
- Streaming for large files

### Frontend Optimization
- Lazy loading components
- Memoized callbacks
- Efficient re-renders
- Progressive enhancement

## Security

### Implemented
- File type validation
- Size limits (100MB default)
- CORS configuration
- Input sanitization

### Future Enhancements
- User authentication
- Rate limiting
- File encryption
- Secure file storage

## Scalability

### Current Architecture
- Single-server deployment
- In-memory job storage
- Local file system

### Future Enhancements
- Redis for job queue
- S3 for file storage
- Horizontal scaling
- Load balancing
- Database for job persistence

## Technology Choices Rationale

### Why Oemer for OMR?
- Open-source and free
- Python-native
- Good accuracy on clean sheets
- Active development

### Why Basic Pitch for AMT?
- State-of-the-art from Spotify
- Multi-instrument support
- No API keys required
- Well-documented

### Why music21?
- Industry standard
- Comprehensive format support
- Excellent documentation
- Large community

### Why FastAPI?
- Modern async support
- Automatic API documentation
- Type safety with Pydantic
- High performance

### Why React + TypeScript?
- Strong typing
- Component reusability
- Large ecosystem
- Developer experience

## Deployment Options

### Development
- Backend: `uvicorn main:app --reload`
- Frontend: `npm start`

### Production
- Backend: Gunicorn + Uvicorn workers
- Frontend: Build and serve with nginx
- Containerization: Docker + Docker Compose
- Cloud: AWS/GCP/Azure with load balancing

## Monitoring & Logging

### Current
- Loguru for structured logging
- Console output for development
- File-based logs (rotation enabled)

### Future
- Application monitoring (Sentry)
- Performance metrics (Prometheus)
- Log aggregation (ELK stack)
- User analytics

---

This architecture provides a solid foundation for the Band Music platform while remaining flexible for future enhancements and scaling needs.
