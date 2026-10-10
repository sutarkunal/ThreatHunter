"""Pydantic schemas for packets."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PacketBase(BaseModel):
    """Base packet schema."""
    timestamp: datetime
    src_ip: str = Field(..., max_length=45)
    dst_ip: str = Field(..., max_length=45)
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    protocol: str = Field(..., max_length=20)
    length: int = Field(..., gt=0)
    flags: Optional[str] = Field(None, max_length=50)
    info: Optional[str] = None


class PacketCreate(PacketBase):
    """Schema for creating a packet."""
    session_id: int


class PacketResponse(PacketBase):
    """Schema for packet response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int


class PacketListResponse(BaseModel):
    """Schema for listing packets."""
    packets: list[PacketResponse]
    total: int
    page: int
    page_size: int
