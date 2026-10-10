"""Packet API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.schemas.packet import PacketListResponse
from app.services.packet_processor import PacketProcessor

router = APIRouter()


@router.get("/packets", response_model=PacketListResponse)
async def list_packets(
    session_id: int = Query(..., description="Session ID"),
    limit: int = Query(100, ge=1, le=1000, description="Number of packets to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    src_ip: Optional[str] = Query(None, description="Filter by source IP"),
    dst_ip: Optional[str] = Query(None, description="Filter by destination IP"),
    protocol: Optional[str] = Query(None, description="Filter by protocol"),
    db: Session = Depends(get_db)
):
    """
    Query packets with optional filters and pagination.
    """
    processor = PacketProcessor(db)

    packets, total = processor.get_packets(
        session_id=session_id,
        limit=limit,
        offset=offset,
        src_ip=src_ip,
        dst_ip=dst_ip,
        protocol=protocol
    )

    return {
        "packets": packets,
        "total": total,
        "page": offset // limit + 1,
        "page_size": limit
    }
