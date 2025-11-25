#!/bin/bash

# Band Music Backend Setup Script

echo "🎵 Setting up Band Music Backend..."

# Check if venv already exists and detect its Python version
if [ -d "venv" ]; then
    echo "📦 Virtual environment detected, checking Python version..."
    python_version=$(./venv/bin/python --version 2>&1 | awk '{print $2}')
    python_major=$(echo $python_version | cut -d. -f1)
    python_minor=$(echo $python_version | cut -d. -f2)
    echo "🐍 Virtual environment Python version: $python_version"
else
    # Check system Python version for guidance
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    python_major=$(echo $python_version | cut -d. -f1)
    python_minor=$(echo $python_version | cut -d. -f2)
    echo "🐍 System Python version: $python_version"
fi

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 9 ]); then
    echo "❌ Python 3.9+ required. Current version: $python_version"
    exit 1
fi

if [ "$python_major" -eq 3 ] && [ "$python_minor" -ge 13 ]; then
    echo "❌ ERROR: Python 3.13+ is not yet supported"
    echo ""
    echo "   The 'basic-pitch' library (AMT pipeline) requires Python 3.9-3.12"
    echo "   Please install Python 3.12 and try again:"
    echo ""
    echo "   macOS:   brew install python@3.12"
    echo "   Linux:   sudo apt install python3.12 python3.12-venv"
    echo ""
    echo "   Then create venv with: python3.12 -m venv venv"
    echo "   Your current venv was created with Python $python_version"
    exit 1
fi

echo "✅ Python version OK"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "📦 Using existing virtual environment..."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and essential build tools
echo "⬆️  Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "📥 Installing Python dependencies (this may take several minutes)..."
echo "Note: Using requirements.txt (recommended - works with Python 3.9-3.12)"
echo "      For legacy exact versions, see: requirements-legacy-python39-312.txt"
pip install -r requirements.txt

# Check for system dependencies
echo ""
echo "🔍 Checking system dependencies..."

# Check for FluidSynth
if ! command -v fluidsynth &> /dev/null; then
    echo "⚠️  FluidSynth not found. Please install it:"
    echo "   macOS: brew install fluidsynth"
    echo "   Linux: sudo apt-get install fluidsynth"
else
    echo "✅ FluidSynth found"
fi

# Check for LilyPond
if ! command -v lilypond &> /dev/null; then
    echo "⚠️  LilyPond not found. Please install it:"
    echo "   macOS: brew install lilypond"
    echo "   Linux: sudo apt-get install lilypond"
else
    echo "✅ LilyPond found"
fi

# Check for Poppler (pdftoimage)
if ! command -v pdftoimage &> /dev/null && ! command -v pdftoppm &> /dev/null; then
    echo "⚠️  Poppler not found. Please install it:"
    echo "   macOS: brew install poppler"
    echo "   Linux: sudo apt-get install poppler-utils"
else
    echo "✅ Poppler found"
fi

# Create .env file from example
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update paths as needed."
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p uploads outputs logs

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the server: uvicorn main:app --reload"
echo ""
