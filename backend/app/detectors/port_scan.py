"""Port scan detector."""
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import and_

from app.detectors.base import BaseDetector
from app.models import Packet
from app.config import get_settings

settings = get_settings()


class PortScanDetector(BaseDetector):
    """
    Detect port scanning activity.

    A port scan is detected when a single source IP attempts to connect
    to many different destination ports within a short time window.
    """

    def get_name(self) -> str:
        return "Port Scan Detector"

    def detect(self) -> List[Dict]:
        """
        Detect port scan attempts.

        Algorithm:
        - Group packets by source IP
        - Count unique destination ports within time window
        - Generate alert if threshold exceeded
        """
        alerts = []

        # Get all packets for this session
        packets = self.db.query(Packet).filter(
            Packet.session_id == self.session_id
        ).order_by(Packet.timestamp).all()

        if not packets:
            return alerts

        # Group by source IP
        ip_activity = defaultdict(list)

        for packet in packets:
            if packet.dst_port:  # Only consider packets with ports
                ip_activity[packet.src_ip].append({
                    'timestamp': packet.timestamp,
                    'dst_port': packet.dst_port,
                    'dst_ip': packet.dst_ip
                })

        # Analyze each source IP
        for src_ip, activity in ip_activity.items():
            # Sort by timestamp
            activity.sort(key=lambda x: x['timestamp'])

            # Sliding window analysis
            time_window = timedelta(seconds=settings.PORT_SCAN_TIME_WINDOW)

            for i, start_packet in enumerate(activity):
                start_time = start_packet['timestamp']
                end_time = start_time + time_window

                # Count unique ports in window
                unique_ports = set()
                unique_dst_ips = set()

                for packet in activity[i:]:
                    if packet['timestamp'] > end_time:
                        break
                    unique_ports.add(packet['dst_port'])
                    unique_dst_ips.add(packet['dst_ip'])

                port_count = len(unique_ports)

                # Check thresholds
                severity = None
                if port_count >= settings.PORT_SCAN_THRESHOLD_HIGH:
                    severity = "high"
                elif port_count >= settings.PORT_SCAN_THRESHOLD_MEDIUM:
                    severity = "medium"

                if severity:
                    alert = self.create_alert(
                        alert_type="port_scan",
                        severity=severity,
                        title=f"Port Scan Detected from {src_ip}",
                        description=(
                            f"Source IP {src_ip} attempted connections to {port_count} "
                            f"unique ports across {len(unique_dst_ips)} destination(s) "
                            f"within {settings.PORT_SCAN_TIME_WINDOW} seconds."
                        ),
                        src_ip=src_ip,
                        metadata=f'{{"port_count": {port_count}, "dst_ip_count": {len(unique_dst_ips)}}}'
                    )
                    alerts.append(alert)
                    break  # Only report once per source IP

        return alerts
