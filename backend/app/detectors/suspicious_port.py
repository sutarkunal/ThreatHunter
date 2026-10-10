"""Suspicious port detector."""
from typing import List, Dict
from collections import defaultdict

from app.detectors.base import BaseDetector
from app.models import Packet
from app.config import get_settings

settings = get_settings()


class SuspiciousPortDetector(BaseDetector):
    """
    Detect connections to commonly abused ports.

    Monitors for connections to ports frequently used by attackers
    such as Telnet, SMB, RDP, etc.
    """

    def get_name(self) -> str:
        return "Suspicious Port Detector"

    def detect(self) -> List[Dict]:
        """
        Detect suspicious port usage.

        Algorithm:
        - Check destination ports against known suspicious ports
        - Generate alert based on port's severity level
        """
        alerts = []

        # Track connections by port and source IP
        port_connections = defaultdict(set)  # port -> set of source IPs

        # Get all packets with destination ports
        packets = self.db.query(Packet).filter(
            Packet.session_id == self.session_id,
            Packet.dst_port.isnot(None)
        ).all()

        for packet in packets:
            if packet.dst_port in settings.SUSPICIOUS_PORTS:
                port_connections[packet.dst_port].add(packet.src_ip)

        # Generate alerts for detected suspicious ports
        for port, src_ips in port_connections.items():
            port_info = settings.SUSPICIOUS_PORTS[port]

            alert = self.create_alert(
                alert_type="suspicious_port",
                severity=port_info["severity"],
                title=f"Suspicious Port Activity Detected: {port_info['name']} (Port {port})",
                description=(
                    f"Detected {len(src_ips)} source IP(s) attempting to connect to "
                    f"port {port} ({port_info['name']}). This port is commonly associated "
                    f"with security vulnerabilities and unauthorized access attempts."
                ),
                metadata=f'{{"port": {port}, "service": "{port_info["name"]}", "src_ip_count": {len(src_ips)}}}'
            )
            alerts.append(alert)

        return alerts
