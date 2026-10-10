"""Pydantic schemas for alerts."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    """Base alert schema."""
    alert_type: str = Field(..., max_length=50)
    severity: str = Field(..., max_length=20)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    src_ip: Optional[str] = Field(None, max_length=45)
    dst_ip: Optional[str] = Field(None, max_length=45)
    metadata: Optional[str] = None


class AlertCreate(AlertBase):
    """Schema for creating an alert."""
    session_id: int
    related_packets: Optional[str] = None


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""
    status: str = Field(..., pattern="^(active|acknowledged|resolved)$")


class AlertResponse(AlertBase):
    """Schema for alert response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    timestamp: datetime
    related_packets: Optional[str]
    status: str


class AlertListResponse(BaseModel):
    """Schema for listing alerts."""
    alerts: list[AlertResponse]
    total: int
