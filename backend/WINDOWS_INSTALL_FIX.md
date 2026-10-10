# ThreatHunter Backend - Windows Installation Fix

## Issue
Some packages require Rust compilation which fails on Windows.

## Solution: Install in stages

### Step 1: Install core dependencies (no compilation needed)
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install python-dateutil==2.8.2
```

### Step 2: Install PyShark (may need tshark installed first)
```bash
pip install pyshark
```

### Alternative: Use requirements-simple.txt
```bash
pip install -r requirements-simple.txt
```

## If you still get Rust errors:

### Option A: Use pre-built wheels
```bash
pip install --only-binary :all: -r requirements-simple.txt
```

### Option B: Skip problematic packages temporarily
The app will run without:
- celery (background tasks - we use BackgroundTasks instead)
- redis (not critical for basic functionality)
- testing packages (pytest, etc.)

Just install the core packages listed in Step 1 above.

## Verify Installation
```bash
python -c "import fastapi; import sqlalchemy; import pyshark; print('✅ Core packages installed!')"
```

## Run the Server
```bash
python run.py
```

Should start on http://localhost:8000
