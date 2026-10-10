"""Excessive requests detector."""
from typing import List, Dict
from collections import defaultdict
from datetime import timedelta

from app.detectors.base import BaseDetector
from app.models import Packet
from app.config import get_settings

settings = get_settings()


class ExcessiveRequestsDetector(BaseDetector):
    """
    Detect source IPs generating excessive requests.

    Identifies IPs that generate an unusually high number of packets,
    which may indicate DDoS attempts, scanning, or other malicious activity.
    """

    def get_name(self) -> str:
        return "Excessive Requests Detector"

    def detect(self) -> List[Dict]:
        """
        Detect excessive request patterns.

        Algorithm:
        - Count packets per source IP within time windows
        - Generate alert if threshold exceeded
        """
        alerts = []

        # Get all packets
        packets = self.db.query(Packet).filter(
            Packet.session_id == self.session_id
        ).order_by(Packet.timestamp).all()

        if not packets:
            return alerts

        # Group by source IP
        ip_activity = defaultdict(list)

        for packet in packets:
            ip_activity[packet.src_ip].append(packet.timestamp)

        # Analyze each source IP
        time_window = timedelta(seconds=settings.EXCESSIVE_REQUESTS_TIME_WINDOW)

        for src_ip, timestamps in ip_activity.items():
            timestamps.sort()

            # Sliding window to find max rate
            max_rate = 0

            for i, start_time in enumerate(timestamps):
                end_time = start_time + time_window

                # Count packets in window
                count = 0
                for ts in timestamps[i:]:
                    if ts > end_time:
                        break
                    count += 1

                max_rate = max(max_rate, count)

            # Check thresholds
            severity = None
            if max_rate >= settings.EXCESSIVE_REQUESTS_HIGH:
                severity = "high"
            elif max_rate >= settings.EXCESSIVE_REQUESTS_MEDIUM:
                severity = "medium"

            if severity:
                alert = self.create_alert(
                    alert_type="excessive_requests",
                    severity=severity,
                    title=f"Excessive Requests from {src_ip}",
                    description=(
                        f"Source IP {src_ip} generated {max_rate} packets within "
                        f"{settings.EXCESSIVE_REQUESTS_TIME_WINDOW} seconds, indicating "
                        f"potentially malicious automated activity or DDoS attempt."
                    ),
                    src_ip=src_ip,
                    metadata=f'{{"max_rate": {max_rate}, "total_packets": {len(timestamps)}}}'
                )
                alerts.append(alert)

        return alerts
