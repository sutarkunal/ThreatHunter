"""Pydantic schemas for API validation."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class SessionBase(BaseModel):
    """Base schema for Session."""
    filename: str = Field(..., min_length=1, max_length=255)


class SessionCreate(SessionBase):
    """Schema for creating a session."""
    file_size: Optional[int] = None


class SessionUpdate(BaseModel):
    """Schema for updating a session."""
    status: Optional[str] = None
    packet_count: Optional[int] = None
    duration: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    unique_src_ips: Optional[int] = None
    unique_dst_ips: Optional[int] = None


class SessionResponse(SessionBase):
    """Schema for session response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    upload_timestamp: datetime
    packet_count: int
    file_size: Optional[int]
    status: str
    duration: Optional[float]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    unique_src_ips: int
    unique_dst_ips: int


class SessionListResponse(BaseModel):
    """Schema for listing sessions."""
    sessions: list[SessionResponse]
    total: int
