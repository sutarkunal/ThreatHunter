from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Session(Base):
    """PCAP session model - represents an uploaded PCAP file."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    upload_timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    packet_count = Column(Integer, default=0)
    file_size = Column(Integer)
    status = Column(String(50), default="processing")  # processing, completed, failed
    duration = Column(Float)  # Duration of capture in seconds
    start_time = Column(DateTime)  # First packet timestamp
    end_time = Column(DateTime)  # Last packet timestamp
    unique_src_ips = Column(Integer, default=0)
    unique_dst_ips = Column(Integer, default=0)

    # Relationships
    packets = relationship("Packet", back_populates="session", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="session", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, filename='{self.filename}', status='{self.status}')>"
