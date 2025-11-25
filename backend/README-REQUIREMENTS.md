# Requirements Files Guide

This project maintains two requirements files to support different Python versions and use cases:

## Files

### `requirements.txt` (Recommended)
**Purpose**: Flexible version ranges for better compatibility with Python 3.9-3.14+

**Use when**:
- Setting up for the first time
- Using Python 3.13 or newer
- Want automatic compatibility with newer Python versions
- Development and testing environments

**Characteristics**:
- Uses version ranges (e.g., `numpy>=1.24.0,<2.0.0`)
- Allows pip to choose compatible versions
- Better forward compatibility
- May result in slightly different versions on different systems

**Example versions it might install**:
- Python 3.14: numpy 1.26.4 (latest with wheels)
- Python 3.11: numpy 1.24.3 (older but stable)

### `requirements-legacy-python39-312.txt`
**Purpose**: Exact versions from original development (Python 3.9-3.12 only)

**Use when**:
- Need to reproduce the exact original development environment
- Debugging a specific issue that worked in the original setup
- Production deployment matching original tested versions
- Using Python 3.9-3.12 ONLY (will fail on Python 3.13+)

**Characteristics**:
- Exact versions (e.g., `numpy==1.24.3`)
- Guaranteed reproducibility
- May require building from source on Python 3.13+
- Same environment every time

**Example**: Always installs numpy 1.24.3 regardless of Python version

## Quick Start

```bash
# Recommended: Use automatic setup script
./setup.sh

# Manual installation with flexible requirements (default)
pip install -r requirements.txt

# Manual installation with legacy exact versions (Python 3.9-3.12 only)
pip install -r requirements-legacy-python39-312.txt
```

## Python Version Compatibility

| Python Version | requirements.txt | requirements-legacy-python39-312.txt |
|---------------|------------------|--------------------------------------|
| 3.9 - 3.12    | ✅ Fast (wheels) | ✅ Fast (wheels)                     |
| 3.13+         | ✅ Works         | ❌ Will fail (incompatible)          |

## Updating Dependencies

### Update flexible requirements (recommended)
```bash
source venv/bin/activate
pip install new-package
pip freeze > requirements.txt
```

### Update legacy requirements (not recommended)
```bash
source venv/bin/activate
pip install new-package==specific.version
pip freeze > requirements-legacy-python39-312.txt
```

**Note**: Most users should update `requirements.txt` instead

## Troubleshooting

### Build failures on Python 3.13+
**Solution**: Use `requirements.txt` (the legacy file doesn't work with Python 3.13+)

### Need exact same environment as original development
**Solution**: Use Python 3.9-3.12 and `requirements-legacy-python39-312.txt`

### Packages taking too long to install
**Solution**: 
1. Downgrade to Python 3.11 or 3.12
2. Or use `requirements.txt` for better compatibility

## System Dependencies

Both files require these system packages:

**macOS**:
```bash
brew install fluidsynth lilypond poppler
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install fluidsynth lilypond poppler-utils
```

## Which Should I Use?

```
┌──────────────────────────────────────────────────────┐
│ Decision Tree                                         │
├──────────────────────────────────────────────────────┤
│                                                       │
│  First time setup?                                    │
│       └─ Use requirements.txt ✅                      │
│                                                       │
│  Need to match original development exactly?          │
│       ├─ Have Python 3.9-3.12?                       │
│       │    └─ Use requirements-legacy-python39-312.txt│
│       └─ Have Python 3.13+?                          │
│            └─ Use requirements.txt (legacy won't work)│
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Default recommendation**: `requirements.txt` (flexible) - works for all Python versions and is selected by `setup.sh`
