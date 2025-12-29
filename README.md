# 🎵 Band Music Helper - Music Conversion Platform

Transform sheet music images into playable audio, and audio files into sheet music scores using AI applications and open-source music libraries.

## ✨ Features

### 🎼 Sheet Music → Audio
Convert sheet music images or PDFs into playable MP3 audio files with your choice of instrument.

**How it works:**
1. **OMR (Oemer):** Extracts musical notation from images
2. **Processing (music21):** Converts MusicXML to MIDI format
3. **Instrument Selection:** Apply instrument program changes (Piano, Trombone, Trumpet)
4. **Synthesis (FluidSynth):** Generates high-quality MP3 audio with selected instrument

**Supported Input:** PNG, JPG, JPEG, PDF  
**Instrument Options:** 🎹 Piano, 🎺 Trombone, 🎺 Trumpet  
**Output:** MP3 audio file

**Note:** For best results with OMR, use sheet music with 1-2 staves. Complex multi-staff scores (3+ staves) may not be processed accurately.

### 🎵 Audio → Sheet Music
Convert audio files into readable PDF sheet music scores.

**How it works:**
1. **AMT (Basic Pitch):** Transcribes audio to MIDI notation
2. **Processing (music21):** Converts MIDI to MusicXML format
3. **Rendering (LilyPond):** Generates professional PDF scores

**Supported Input:** MP3, WAV, OGG, M4A, FLAC  
**Output:** PDF sheet music score

## Why I Built This

I'm in band, and I wanted a tool that could help me practice by converting sheet music to audio with different instruments. The issue was that there wasn't a simple way to take a photo of sheet music and hear how it should sound with different instruments.

Building this was harder than I expected. The main challenge was handling reliability. Music notation software can be sensitive to input quality, and making sure the system handled errors well without crashing was important. I also had to figure out how to manage processing queues, since some conversions can take time and you don't want the system to lock up while processing.

## 🛠 Technology Stack

### Backend
- **Framework:** FastAPI (Python)
- **OMR:** [Oemer](https://github.com/BreezeWhite/oemer) - Optical Music Recognition
- **AMT:** [Basic Pitch](https://github.com/spotify/basic-pitch) - Spotify's audio transcription
- **Processing:** [music21](https://web.mit.edu/music21/) - Music notation toolkit
- **Synthesis:** FluidSynth + midi2audio + mido - MIDI to audio conversion
- **Rendering:** [LilyPond](https://lilypond.org/) - Music engraving
- **Logging:** Loguru for debugging and monitoring

### Frontend
- **Framework:** React 18 with TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Build Tool:** Create React App

## 📁 Project Structure

```
band-music-helper/
├── backend/                 # Python FastAPI server
│   ├── src/
│   │   ├── omr/            # Optical Music Recognition
│   │   ├── amt/            # Automatic Music Transcription
│   │   ├── processing/     # Music format conversions
│   │   │   ├── converter.py    # MusicXML ↔ MIDI
│   │   │   ├── synthesizer.py  # MIDI → Audio
│   │   │   └── renderer.py     # MusicXML → PDF
│   │   ├── pipeline/       # Processing pipelines
│   │   └── config/         # Settings and configuration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # Temporary uploads
│   └── outputs/            # Generated files
│
└── frontend/               # React TypeScript app
    ├── src/
    │   ├── components/     # React components
    │   ├── services/       # API integration
    │   └── App.tsx         # Main application
    └── package.json        # Node dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9-3.12**
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

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and update paths as needed
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Server will be available at: http://localhost:8000

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

### Sheet Music → Audio

**Upload Image/PDF:**
```http
POST /api/omr/upload?instrument={piano|trombone|trumpet}
```
Query Parameters:
- `instrument` (optional): Instrument for audio synthesis - `piano` (default), `trombone`, or `trumpet`

**Check Status:**
```http
GET /api/omr/status/{job_id}
```

**Download Result:**
```http
GET /api/omr/download/{job_id}
```

### Audio → Sheet Music

**Upload Audio:**
```http
POST /api/amt/upload
```

**Check Status:**
```http
GET /api/amt/status/{job_id}
```

**Download Result:**
```http
GET /api/amt/download/{job_id}
```

## 📝 What I Learned

Building this taught me about infrastructure and reliability. When you're working with AI applications that process files, you have to think about what happens when things fail. The system needs to handle timeouts, partial failures, and edge cases without crashing or losing data.

I also learned about trade-offs in system design. You can make things faster by processing everything immediately, but that makes the system less reliable. Using queues and status tracking makes it more complex, but it handles errors better and gives users feedback on what's happening.

Testing with real-world inputs (different sheet music quality, various audio formats) helped me identify issues I wouldn't have caught otherwise. For example, I found that some sheet music scans needed preprocessing to work reliably, and certain audio formats required special handling.

## 🐛 Troubleshooting

### Common Issues

**FluidSynth soundfont not found**
- Update `FLUIDSYNTH_SOUNDFONT` path in `.env`
- Download a soundfont: https://musical-artifacts.com/artifacts?tags=soundfont

**LilyPond command not found**
- Ensure LilyPond is installed and in PATH
- macOS: `brew install lilypond`

**PDF conversion fails (poppler)**
- Install poppler-utils
- macOS: `brew install poppler`

**Python import errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Libraries Used

- **[Oemer](https://github.com/BreezeWhite/oemer)** - Optical Music Recognition
- **[Basic Pitch](https://github.com/spotify/basic-pitch)** - Automatic Music Transcription by Spotify
- **[music21](https://web.mit.edu/music21/)** - Music notation toolkit
- **[FluidSynth](http://www.fluidsynth.org/)** - Software synthesizer
- **[LilyPond](https://lilypond.org/)** - Music engraving program
- **[FastAPI](https://fastapi.tiangolo.com/)** - Python web framework
- **[React](https://react.dev/)** - Frontend JavaScript library

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

If you find issues or have suggestions, feel free to open an issue. I'm continuing to improve this project based on real usage.

---

**Note:** This project requires computational resources for audio transcription. Processing times may vary based on file size and system specifications.
