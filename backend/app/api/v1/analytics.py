"""Analytics API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict
from datetime import datetime, timedelta

from app.database.session import get_db
from app.models import Packet, Alert, Session as SessionModel
from app.schemas.analytics import (
    OverviewAnalytics,
    TrafficOverTime,
    ProtocolDistributionResponse,
    TopIP,
    ProtocolDistribution,
    TimeseriesData
)

router = APIRouter()


@router.get("/analytics/overview", response_model=OverviewAnalytics)
async def get_overview_analytics(
    session_id: int = Query(..., description="Session ID"),
    db: Session = Depends(get_db)
):
    """
    Get overview analytics for a session.
    """
    # Verify session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Total packets
    total_packets = db.query(func.count(Packet.id)).filter(
        Packet.session_id == session_id
    ).scalar()

    # Total alerts
    total_alerts = db.query(func.count(Alert.id)).filter(
        Alert.session_id == session_id
    ).scalar()

    # Active threats
    active_threats = db.query(func.count(Alert.id)).filter(
        Alert.session_id == session_id,
        Alert.status == "active"
    ).scalar()

    # Protocol distribution
    protocol_counts = db.query(
        Packet.protocol,
        func.count(Packet.id)
    ).filter(
        Packet.session_id == session_id
    ).group_by(Packet.protocol).all()

    protocols = {proto: count for proto, count in protocol_counts}

    # Top source IPs
    top_src_ips = db.query(
        Packet.src_ip,
        func.count(Packet.id).label('count')
    ).filter(
        Packet.session_id == session_id
    ).group_by(Packet.src_ip).order_by(func.count(Packet.id).desc()).limit(10).all()

    # Top destination IPs
    top_dst_ips = db.query(
        Packet.dst_ip,
        func.count(Packet.id).label('count')
    ).filter(
        Packet.session_id == session_id
    ).group_by(Packet.dst_ip).order_by(func.count(Packet.id).desc()).limit(10).all()

    return {
        "session_id": session_id,
        "total_packets": total_packets or 0,
        "total_alerts": total_alerts or 0,
        "active_threats": active_threats or 0,
        "protocols": protocols,
        "top_src_ips": [TopIP(ip=ip, count=count) for ip, count in top_src_ips],
        "top_dst_ips": [TopIP(ip=ip, count=count) for ip, count in top_dst_ips]
    }


@router.get("/analytics/protocol-distribution", response_model=ProtocolDistributionResponse)
async def get_protocol_distribution(
    session_id: int = Query(..., description="Session ID"),
    db: Session = Depends(get_db)
):
    """
    Get protocol distribution for a session.
    """
    # Get protocol counts
    protocol_counts = db.query(
        Packet.protocol,
        func.count(Packet.id)
    ).filter(
        Packet.session_id == session_id
    ).group_by(Packet.protocol).all()

    total = sum(count for _, count in protocol_counts)

    if total == 0:
        return {"protocols": []}

    protocols = [
        ProtocolDistribution(
            protocol=proto,
            count=count,
            percentage=round((count / total) * 100, 2)
        )
        for proto, count in protocol_counts
    ]

    return {"protocols": protocols}


@router.get("/analytics/traffic-over-time", response_model=TrafficOverTime)
async def get_traffic_over_time(
    session_id: int = Query(..., description="Session ID"),
    interval_seconds: int = Query(60, ge=1, le=3600, description="Time interval in seconds"),
    db: Session = Depends(get_db)
):
    """
    Get traffic volume over time.
    """
    # Get all packets with timestamps
    packets = db.query(
        Packet.timestamp,
        Packet.length
    ).filter(
        Packet.session_id == session_id
    ).order_by(Packet.timestamp).all()

    if not packets:
        return {"timeseries": []}

    # Group by time intervals
    time_buckets = defaultdict(lambda: {"count": 0, "bytes": 0})

    for timestamp, length in packets:
        # Round timestamp to interval
        bucket_time = timestamp.replace(second=0, microsecond=0)
        time_buckets[bucket_time]["count"] += 1
        time_buckets[bucket_time]["bytes"] += length

    # Create timeseries data
    timeseries = [
        TimeseriesData(
            timestamp=ts,
            packet_count=data["count"],
            bytes=data["bytes"]
        )
        for ts, data in sorted(time_buckets.items())
    ]

    return {"timeseries": timeseries}
