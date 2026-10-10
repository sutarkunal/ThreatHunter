from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class Packet(Base):
    """Packet model - represents individual network packets."""

    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    src_ip = Column(String(45), nullable=False, index=True)  # IPv4 or IPv6
    dst_ip = Column(String(45), nullable=False, index=True)
    src_port = Column(Integer)
    dst_port = Column(Integer)
    protocol = Column(String(20), nullable=False)
    length = Column(Integer, nullable=False)
    flags = Column(String(50))  # TCP flags
    info = Column(Text)  # Additional packet info

    # Relationships
    session = relationship("Session", back_populates="packets")

    def __repr__(self):
        return f"<Packet(id={self.id}, {self.src_ip}:{self.src_port} -> {self.dst_ip}:{self.dst_port})>"
