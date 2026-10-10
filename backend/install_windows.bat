@echo off
echo Installing ThreatHunter Backend Dependencies for Windows...
echo.

echo Step 1: Installing FastAPI and core web framework...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6

echo.
echo Step 2: Installing database dependencies...
pip install sqlalchemy==2.0.23

echo.
echo Step 3: Installing validation and utilities...
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install python-dateutil==2.8.2

echo.
echo Step 4: Installing PyShark for PCAP parsing...
pip install pyshark

echo.
echo ✅ Installation complete!
echo.
echo To verify, run: python -c "import fastapi; import sqlalchemy; import pyshark; print('All core packages installed!')"
echo.
echo To start the server: python run.py
pause
