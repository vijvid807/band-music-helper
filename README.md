# 🎵 Band Music - Music Conversion Platform

Transform sheet music images into playable audio, and audio files into sheet music scores using AI and open-source music libraries.

## 📖 Documentation

- **[README.md](README.md)** (this file) - Complete project overview and setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical architecture
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guidelines and best practices
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Detailed implementation summary
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Recent architectural improvements
- **Backend Docs:**
  - [backend/REFACTORING.md](backend/REFACTORING.md) - Backend architecture patterns
  - [backend/QUICKSTART.md](backend/QUICKSTART.md) - Backend-specific setup
- **Frontend Docs:**
  - [frontend/REFACTORING.md](frontend/REFACTORING.md) - Frontend architecture patterns
  - [frontend/README.md](frontend/README.md) - Frontend-specific documentation

## ✨ Features

### 🎼 Use Case 1: Sheet Music → Audio
Convert sheet music images or PDFs into playable MP3 audio files with your choice of instrument.

**Pipeline:**
1. **OMR (Oemer):** Extracts musical notation from images
2. **Processing (music21):** Converts MusicXML to MIDI format
3. **Instrument Selection:** Apply instrument program changes (Piano, Trombone, Trumpet)
4. **Synthesis (FluidSynth):** Generates high-quality MP3 audio with selected instrument

**Supported Input:** PNG, JPG, JPEG, PDF  
**Instrument Options:** 🎹 Piano, 🎺 Trombone, 🎺 Trumpet  
**Output:** MP3 audio file

**Note:** For best results with OMR, use sheet music with 1-2 staves. Complex multi-staff scores (3+ staves) may not be processed accurately.

### 🎵 Use Case 2: Audio → Sheet Music
Convert audio files into readable PDF sheet music scores.

**Pipeline:**
1. **AMT (Basic Pitch):** Transcribes audio to MIDI notation
2. **Processing (music21):** Converts MIDI to MusicXML format
3. **Rendering (LilyPond):** Generates professional PDF scores

**Supported Input:** MP3, WAV, OGG, M4A, FLAC  
**Output:** PDF sheet music score

## 📁 Project Structure

```
band-music/
├── backend/                 # Python FastAPI server
│   ├── src/
│   │   ├── omr/            # Optical Music Recognition
│   │   │   └── processor.py
│   │   ├── amt/            # Automatic Music Transcription
│   │   │   └── processor.py
│   │   ├── processing/     # Music format conversions
│   │   │   ├── converter.py    # MusicXML ↔ MIDI
│   │   │   ├── synthesizer.py  # MIDI → Audio
│   │   │   └── renderer.py     # MusicXML → PDF
│   │   ├── pipeline/       # Processing pipelines
│   │   │   ├── omr_pipeline.py
│   │   │   └── amt_pipeline.py
│   │   └── config/         # Settings and configuration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt         # Python dependencies (flexible versions)
│   ├── requirements-pinned.txt  # Pinned versions for reproducibility
│   ├── setup.sh            # Setup script
│   ├── uploads/            # Temporary uploads
│   ├── outputs/            # Generated files
│   └── logs/               # Application logs
│
└── frontend/               # React TypeScript app
    ├── src/
    │   ├── components/     # React components
    │   │   ├── OMRConverter.tsx
    │   │   └── AMTConverter.tsx
    │   ├── services/       # API integration
    │   │   └── api.ts
    │   ├── App.tsx         # Main application
    │   └── index.tsx       # Entry point
    ├── public/             # Static assets
    ├── package.json        # Node dependencies
    └── tailwind.config.js  # Tailwind CSS config
```

## 🛠 Technology Stack

### Backend
- **Framework:** FastAPI 0.109+ (Python)
- **OMR:** [Oemer](https://github.com/BreezeWhite/oemer) - Optical Music Recognition
- **AMT:** [Basic Pitch](https://github.com/spotify/basic-pitch) - Spotify's audio transcription
- **Processing:** [music21](https://web.mit.edu/music21/) - Music notation toolkit
- **Synthesis:** FluidSynth + midi2audio + mido - MIDI to audio conversion with instrument selection
- **Rendering:** [LilyPond](https://lilypond.org/) - Music engraving
- **Logging:** Loguru
- **Validation:** Pydantic

### Frontend
- **Framework:** React 18+ with TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Build Tool:** Create React App

## 🚀 Quick Start

### Prerequisites

#### Required Software
- **Python 3.9-3.12** ⚠️ *Python 3.13+ not yet supported* - see [PYTHON_VERSION.md](backend/PYTHON_VERSION.md)
- **Node.js 18+**
- **npm or yarn**

#### System Dependencies

**macOS:**
```bash
brew install fluidsynth lilypond poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install fluidsynth lilypond poppler-utils
```

**Windows:**
- Install FluidSynth: [Download](http://www.fluidsynth.org/)
- Install LilyPond: [Download](https://lilypond.org/download.html)
- Install Poppler: [Download](https://blog.alivate.com.au/poppler-windows/)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Run setup script (recommended):**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create environment file
   cp .env.example .env
   # Edit .env and update paths as needed
   
   # Create directories
   mkdir -p uploads outputs logs
   ```

3. **Start the server:**
   ```bash
   source venv/bin/activate  # If not already activated
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Server will be available at: http://localhost:8000
   API documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Start development server:**
   ```bash
   npm start
   ```

   Application will open at: http://localhost:3000

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```
Returns server health status.

### OMR Pipeline (Sheet Music → Audio)

**Upload Image/PDF:**
```http
POST /api/omr/upload?instrument={piano|trombone|trumpet}
Content-Type: multipart/form-data

file: [image/PDF file]
```
Query Parameters:
- `instrument` (optional): Instrument for audio synthesis - `piano` (default), `trombone`, or `trumpet`

Returns: `{ job_id, status, message }`

**Check Status:**
```http
GET /api/omr/status/{job_id}
```
Returns: `{ type, status, filename, progress, step, error }`

**Download Result:**
```http
GET /api/omr/download/{job_id}
```
Returns: MP3 audio file

### AMT Pipeline (Audio → Sheet Music)

**Upload Audio:**
```http
POST /api/amt/upload
Content-Type: multipart/form-data

file: [audio file]
```
Returns: `{ job_id, status, message }`

**Check Status:**
```http
GET /api/amt/status/{job_id}
```
Returns: `{ type, status, filename, progress, step, error }`

**Download Result:**
```http
GET /api/amt/download/{job_id}
```
Returns: PDF score file

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Debug mode
DEBUG=true

# FluidSynth soundfont path (adjust for your system)
FLUIDSYNTH_SOUNDFONT=/usr/share/sounds/sf2/FluidR3_GM.sf2

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# File upload limits
MAX_UPLOAD_SIZE=104857600

# Cleanup intermediate files
CLEANUP_FILES=true
```

### Frontend Configuration

Edit `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
```

## 📝 Usage Examples

### Using the Web Interface

1. Open http://localhost:3000
2. Select a tab:
   - **Sheet Music → Audio:** Upload sheet music image/PDF
   - **Audio → Sheet Music:** Upload audio file
3. Click "Convert" button
4. Wait for processing (progress bar shows status)
5. Download the result when complete

### Using the API (curl)

**Convert sheet music to audio:**
```bash
# Upload (default piano)
curl -X POST http://localhost:8000/api/omr/upload \
  -F "file=@sheet_music.png"

# Upload with instrument selection
curl -X POST "http://localhost:8000/api/omr/upload?instrument=trumpet" \
  -F "file=@sheet_music.png"

# Check status
curl http://localhost:8000/api/omr/status/{job_id}

# Download result
curl -o output.mp3 http://localhost:8000/api/omr/download/{job_id}
```

**Convert audio to sheet music:**
```bash
# Upload
curl -X POST http://localhost:8000/api/amt/upload \
  -F "file=@song.mp3"

# Check status
curl http://localhost:8000/api/amt/status/{job_id}

# Download result
curl -o score.pdf http://localhost:8000/api/amt/download/{job_id}
```

## 🧪 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --log-level debug
```

### Frontend Development

```bash
cd frontend
npm start
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🐛 Troubleshooting

### Common Issues

**1. FluidSynth soundfont not found**
- Update `FLUIDSYNTH_SOUNDFONT` path in `.env`
- Download a soundfont: https://musical-artifacts.com/artifacts?tags=soundfont

**2. LilyPond command not found**
- Ensure LilyPond is installed and in PATH
- macOS: `brew install lilypond`
- Linux: `apt-get install lilypond`

**3. PDF conversion fails (poppler)**
- Install poppler-utils
- macOS: `brew install poppler`
- Linux: `apt-get install poppler-utils`

**4. Python import errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt` (or `requirements-pinned.txt` for exact versions)

**5. CORS errors in browser**
- Check backend is running on port 8000
- Verify `CORS_ORIGINS` in backend `.env`
- Clear browser cache

## 📚 Libraries & Credits

- **[Oemer](https://github.com/BreezeWhite/oemer)** - Optical Music Recognition
- **[Basic Pitch](https://github.com/spotify/basic-pitch)** - Automatic Music Transcription by Spotify
- **[music21](https://web.mit.edu/music21/)** - Music notation toolkit
- **[FluidSynth](http://www.fluidsynth.org/)** - Software synthesizer
- **[LilyPond](https://lilypond.org/)** - Music engraving program
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://react.dev/)** - Frontend JavaScript library

## 📂 Project Structure

```
band-music/
├── README.md                    # Main project documentation (you are here)
├── QUICKSTART.md               # Quick start guide
├── ARCHITECTURE.md             # System architecture
├── DEVELOPMENT.md              # Developer guide
├── PROJECT_SUMMARY.md          # Implementation summary
├── REFACTORING_SUMMARY.md      # Refactoring documentation
├── backend/                    # Python FastAPI backend
│   ├── src/                    # Source code
│   │   ├── core/              # DI container & dependencies
│   │   ├── services/          # Business logic services
│   │   ├── api/               # API routes & models
│   │   ├── omr/               # Optical Music Recognition
│   │   ├── amt/               # Automatic Music Transcription
│   │   ├── processing/        # Music format conversions
│   │   ├── pipeline/          # Processing pipelines
│   │   └── config/            # Configuration
│   ├── main.py                # FastAPI application (legacy)
│   ├── main_refactored.py     # Refactored FastAPI app
│   ├── requirements.txt                      # Python dependencies (recommended)
│   ├── requirements-legacy-python39-312.txt # Legacy exact versions
│   ├── REFACTORING.md         # Backend architecture guide
│   └── QUICKSTART.md          # Backend setup guide
└── frontend/                   # React TypeScript frontend
    ├── src/
    │   ├── components/        # React components
    │   │   ├── common/        # Reusable UI components
    │   │   ├── OMRConverter.tsx
    │   │   └── AMTConverter.tsx
    │   ├── hooks/             # Custom React hooks
    │   ├── contexts/          # React contexts
    │   ├── services/          # API integration
    │   └── App.tsx            # Main application
    ├── package.json           # Node dependencies
    ├── REFACTORING.md         # Frontend architecture guide
    └── README.md              # Frontend documentation
```

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

Built with ❤️ using open-source music AI and notation libraries.

---

**Note:** This project requires significant computational resources for audio transcription (AMT). Processing times may vary based on file size and system specifications.
