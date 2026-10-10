"""Session API endpoints."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database.session import get_db
from app.models import Session as SessionModel
from app.schemas.session import SessionResponse, SessionListResponse, SessionCreate
from app.services.packet_processor import PacketProcessor
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/sessions/upload", response_model=SessionResponse, status_code=201)
async def upload_pcap(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PCAP file for analysis.

    The file will be processed in the background and packets will be extracted.
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Validate file size (check content length if available)
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create session record
    session = SessionModel(
        filename=file.filename,
        file_size=file_size,
        status="processing"
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Process PCAP in background
    processor = PacketProcessor(db)
    background_tasks.add_task(processor.process_pcap, session.id, file_path)

    return session


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(db: Session = Depends(get_db)):
    """
    List all PCAP sessions.
    """
    sessions = db.query(SessionModel).order_by(SessionModel.upload_timestamp.desc()).all()

    return {
        "sessions": sessions,
        "total": len(sessions)
    }


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific session.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: int, db: Session = Depends(get_db)):
    """
    Delete a session and all its associated data.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Delete session (cascades to packets, alerts, reports)
    db.delete(session)
    db.commit()

    return None
