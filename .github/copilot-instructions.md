# Band Music Project - Copilot Instructions

## Project Overview
A full-stack application for music conversion with two main use cases:
1. Image/PDF → Playable Music (OMR pipeline)
2. Audio File → PDF Score (AMT pipeline)

## Progress Checklist

- [x] Verify copilot-instructions.md created
- [ ] Clarify Project Requirements
- [ ] Scaffold the Project (Backend: Python FastAPI, Frontend: React TypeScript)
- [ ] Customize the Project
- [ ] Install Required Extensions
- [ ] Compile the Project
- [ ] Create and Run Task
- [ ] Launch the Project
- [ ] Ensure Documentation is Complete

## Project Requirements

**Backend (Python FastAPI):**
- Use Case 1: Image/PDF → MP3
  - OMR: Oemer or Audiveris
  - Processing: music21 (MusicXML → MIDI)
  - Synthesis: MIDI → MP3
- Use Case 2: Audio → PDF Score
  - AMT: Basic Pitch or Omnizart (MP3/WAV → MIDI)
  - Processing: music21 (MIDI → MusicXML)
  - Rendering: LilyPond (MusicXML → PDF)

**Frontend (React TypeScript):**
- Modern architecture with custom hooks
- File upload with drag-and-drop
- Progress tracking for long-running operations
- Download results
- Support both use cases in unified interface

## Technology Stack
- Backend: Python 3.9+, FastAPI, music21, Oemer/Basic Pitch
- Frontend: React 18+, TypeScript, Tailwind CSS, Axios
- Storage: Local file system for uploads/outputs
