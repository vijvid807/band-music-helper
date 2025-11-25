# Python Version Compatibility

## Current Status (November 2024)

### Supported: Python 3.9 - 3.12 ✅
All features work perfectly with pre-built wheels for fast installation.

### Not Supported: Python 3.13+ ❌
The `basic-pitch` library (used for AMT - Audio to MusicXML pipeline) currently only supports Python up to 3.12.

## Quick Fix

### macOS
```bash
# Install Python 3.12
brew install python@3.12

# Create virtual environment
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)
```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv

# Create virtual environment
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```powershell
# Download and install Python 3.12 from python.org
# Then:
cd backend
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Why This Limitation?

The AMT pipeline depends on:
- **basic-pitch** (Spotify's audio transcription library)
- **TensorFlow** (machine learning framework)

TensorFlow has historically been slow to support the newest Python versions. As of November 2024:
- TensorFlow 2.15+ supports Python 3.11-3.12
- TensorFlow doesn't yet have builds for Python 3.13+

## Will This Change?

Yes! Once TensorFlow releases Python 3.13+ support, we can update. Monitor:
- [TensorFlow releases](https://github.com/tensorflow/tensorflow/releases)
- [Basic-pitch releases](https://github.com/spotify/basic-pitch/releases)

## Alternative: OMR-Only Setup

If you only need the OMR pipeline (Image/PDF → Audio), you can remove the AMT dependencies and use Python 3.13+:

```bash
# Edit requirements.txt and remove/comment out:
# basic-pitch
# tensorflow-related packages

# Then install
pip install -r requirements.txt
```

**Note**: This disables the AMT pipeline (Audio → Sheet Music conversion).

## Checking Your Python Version

```bash
python3 --version
# or
python3.12 --version
```

## Recommendation

**Use Python 3.12** - it's the latest stable version with full package support and will be maintained until 2028.
