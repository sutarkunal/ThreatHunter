from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Alert(Base):
    """Alert model - represents detected security threats."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    alert_type = Column(String(50), nullable=False, index=True)  # port_scan, traffic_spike, etc.
    severity = Column(String(20), nullable=False, index=True)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    description = Column(Text)
    src_ip = Column(String(45))
    dst_ip = Column(String(45))
    related_packets = Column(Text)  # Comma-separated packet IDs
    metadata = Column(Text)  # JSON string with additional data
    status = Column(String(20), default="active")  # active, acknowledged, resolved

    # Relationships
    session = relationship("Session", back_populates="alerts")

    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.alert_type}', severity='{self.severity}')>"
