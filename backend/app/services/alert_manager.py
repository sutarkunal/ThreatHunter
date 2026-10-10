"""Alert management service."""
import logging
from typing import List
from sqlalchemy.orm import Session

from app.models import Alert
from app.detectors import (
    PortScanDetector,
    TrafficSpikeDetector,
    SuspiciousPortDetector,
    ExcessiveRequestsDetector
)

logger = logging.getLogger(__name__)


class AlertManager:
    """Service for managing threat detection and alerts."""

    def __init__(self, db: Session):
        """
        Initialize alert manager.

        Args:
            db: Database session
        """
        self.db = db

    def run_threat_detection(self, session_id: int) -> int:
        """
        Run all threat detectors on a session and store alerts.

        Args:
            session_id: Session ID to analyze

        Returns:
            Number of alerts generated
        """
        logger.info(f"Running threat detection for session {session_id}")

        # Initialize detectors
        detectors = [
            PortScanDetector(self.db, session_id),
            TrafficSpikeDetector(self.db, session_id),
            SuspiciousPortDetector(self.db, session_id),
            ExcessiveRequestsDetector(self.db, session_id)
        ]

        all_alerts = []

        # Run each detector
        for detector in detectors:
            try:
                logger.info(f"Running {detector.get_name()}")
                alerts = detector.detect()
                all_alerts.extend(alerts)
                logger.info(f"{detector.get_name()} found {len(alerts)} alerts")
            except Exception as e:
                logger.error(f"Error in {detector.get_name()}: {e}")

        # Store alerts in database
        alert_count = 0
        for alert_data in all_alerts:
            alert = Alert(**alert_data)
            self.db.add(alert)
            alert_count += 1

        self.db.commit()

        logger.info(f"Generated {alert_count} total alerts for session {session_id}")

        return alert_count

    def get_alerts_by_session(self, session_id: int) -> List[Alert]:
        """
        Get all alerts for a session.

        Args:
            session_id: Session ID

        Returns:
            List of alerts
        """
        return self.db.query(Alert).filter(
            Alert.session_id == session_id
        ).order_by(Alert.timestamp.desc()).all()

    def get_active_threats(self, session_id: int) -> List[Alert]:
        """
        Get active threats for a session.

        Args:
            session_id: Session ID

        Returns:
            List of active alerts
        """
        return self.db.query(Alert).filter(
            Alert.session_id == session_id,
            Alert.status == "active"
        ).all()

    def acknowledge_alert(self, alert_id: int) -> bool:
        """
        Acknowledge an alert.

        Args:
            alert_id: Alert ID

        Returns:
            Success status
        """
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()

        if not alert:
            return False

        alert.status = "acknowledged"
        self.db.commit()

        return True

    def resolve_alert(self, alert_id: int) -> bool:
        """
        Resolve an alert.

        Args:
            alert_id: Alert ID

        Returns:
            Success status
        """
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()

        if not alert:
            return False

        alert.status = "resolved"
        self.db.commit()

        return True
