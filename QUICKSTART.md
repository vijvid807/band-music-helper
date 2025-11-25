# Band Music - Quick Start Guide

This guide will help you get the Band Music application running quickly.

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9 or higher (`python3 --version`)
- [ ] Node.js 18 or higher (`node --version`)
- [ ] npm or yarn (`npm --version`)

## System Dependencies

### macOS
```bash
brew install fluidsynth lilypond poppler
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install fluidsynth lilypond poppler-utils
```

## Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Run automated setup:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Activate environment and start server:**
   ```bash
   source venv/bin/activate
   uvicorn main:app --reload
   ```

   ✅ Backend running at: http://localhost:8000

## Frontend Setup

1. **Navigate to frontend:**
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

   ✅ Frontend running at: http://localhost:3000

## Verify Installation

1. Open http://localhost:3000 in your browser
2. Check backend health: http://localhost:8000/api/health
3. View API docs: http://localhost:8000/docs

## First Conversion Test

### Test OMR (Sheet Music → Audio)
1. Click "Sheet Music → Audio" tab
2. Select your preferred instrument (Piano, Trombone, or Trumpet)
3. Upload a sheet music image (PNG/JPG) or PDF
   - **Tip:** Use simple 1-2 staff music for best results
   - Single melody lines work best (trumpet/trombone solos, simple piano pieces)
4. Click "Convert to Audio"
5. Wait for processing (progress bar shows status)
6. Download MP3 when complete - audio will play with your selected instrument!

### Test AMT (Audio → Sheet Music)
1. Click "Audio → Sheet Music" tab
2. Upload an audio file (MP3/WAV)
3. Click "Convert to Sheet Music"
4. Wait for processing
5. Download PDF score when complete

## Troubleshooting

### Backend won't start
- Check virtual environment is activated: `source venv/bin/activate`
- Verify all dependencies installed: `pip install -r requirements.txt`
  - Use `requirements-pinned.txt` if you need exact version reproducibility (Python 3.9-3.12)
- Check Python version: `python3 --version` (need 3.9+)

### Frontend won't start
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node version: `node --version` (need 18+)

### FluidSynth errors
- Update soundfont path in `backend/.env`
- Download soundfont if needed: https://musical-artifacts.com/artifacts?tags=soundfont

### LilyPond not found
- Ensure LilyPond is installed: `lilypond --version`
- Add to PATH if needed

### CORS errors
- Ensure backend is running on port 8000
- Check CORS_ORIGINS in backend/.env
- Clear browser cache and reload

## Need Help?

- Check the main README.md for detailed documentation
- View API documentation at http://localhost:8000/docs
- Check logs in `backend/logs/app.log`

## Development Mode

For development with hot-reload:

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --log-level debug
```

**Frontend:**
```bash
cd frontend
npm start
```

Both will automatically reload when you make changes to the code.

---

Happy music converting! 🎵
