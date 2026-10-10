from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Report(Base):
    """Report model - represents generated incident reports."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    report_type = Column(String(50), default="incident")
    summary = Column(Text)
    alert_count = Column(Integer)
    threat_summary = Column(Text)  # JSON string
    top_ips = Column(Text)  # JSON string
    file_path = Column(String(500))

    # Relationships
    session = relationship("Session", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, session_id={self.session_id}, type='{self.report_type}')>"
