"""Base detector interface."""
from abc import ABC, abstractmethod
from typing import List, Dict
from sqlalchemy.orm import Session


class BaseDetector(ABC):
    """Base class for all threat detectors."""

    def __init__(self, db: Session, session_id: int):
        """
        Initialize detector.

        Args:
            db: Database session
            session_id: PCAP session ID to analyze
        """
        self.db = db
        self.session_id = session_id

    @abstractmethod
    def detect(self) -> List[Dict]:
        """
        Run detection algorithm.

        Returns:
            List of alert dictionaries
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get detector name."""
        pass

    def create_alert(
        self,
        alert_type: str,
        severity: str,
        title: str,
        description: str,
        src_ip: str = None,
        dst_ip: str = None,
        metadata: str = None,
        related_packets: str = None
    ) -> Dict:
        """
        Create an alert dictionary.

        Args:
            alert_type: Type of alert
            severity: Severity level (low, medium, high, critical)
            title: Alert title
            description: Alert description
            src_ip: Source IP address
            dst_ip: Destination IP address
            metadata: JSON metadata
            related_packets: Comma-separated packet IDs

        Returns:
            Alert dictionary
        """
        return {
            "session_id": self.session_id,
            "alert_type": alert_type,
            "severity": severity,
            "title": title,
            "description": description,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "metadata": metadata,
            "related_packets": related_packets
        }
