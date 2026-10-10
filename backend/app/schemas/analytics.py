"""Pydantic schemas for analytics."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProtocolDistribution(BaseModel):
    """Protocol distribution data."""
    protocol: str
    count: int
    percentage: float


class TopIP(BaseModel):
    """Top IP data."""
    ip: str
    count: int


class TimeseriesData(BaseModel):
    """Timeseries data point."""
    timestamp: datetime
    packet_count: int
    bytes: int


class OverviewAnalytics(BaseModel):
    """Overview analytics response."""
    session_id: int
    total_packets: int
    total_alerts: int
    active_threats: int
    protocols: dict[str, int]
    top_src_ips: list[TopIP]
    top_dst_ips: list[TopIP]


class TrafficOverTime(BaseModel):
    """Traffic over time response."""
    timeseries: list[TimeseriesData]


class ProtocolDistributionResponse(BaseModel):
    """Protocol distribution response."""
    protocols: list[ProtocolDistribution]
