"""Alert API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.models import Alert
from app.schemas.alert import AlertListResponse, AlertResponse, AlertUpdate

router = APIRouter()


@router.get("/alerts", response_model=AlertListResponse)
async def list_alerts(
    session_id: Optional[int] = Query(None, description="Filter by session ID"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    List alerts with optional filters.
    """
    query = db.query(Alert)

    # Apply filters
    if session_id:
        query = query.filter(Alert.session_id == session_id)
    if severity:
        query = query.filter(Alert.severity == severity)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    if status:
        query = query.filter(Alert.status == status)

    alerts = query.order_by(Alert.timestamp.desc()).all()

    return {
        "alerts": alerts,
        "total": len(alerts)
    }


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific alert.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return alert


@router.patch("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    update_data: AlertUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an alert's status.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = update_data.status
    db.commit()
    db.refresh(alert)

    return alert
