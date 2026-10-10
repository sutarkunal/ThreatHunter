"""Traffic spike detector."""
from typing import List, Dict
from collections import defaultdict
from datetime import timedelta

from app.detectors.base import BaseDetector
from app.models import Packet
from app.config import get_settings

settings = get_settings()


class TrafficSpikeDetector(BaseDetector):
    """
    Detect unusual spikes in traffic volume.

    A traffic spike is detected when packet rate significantly exceeds
    the baseline average for the session.
    """

    def get_name(self) -> str:
        return "Traffic Spike Detector"

    def detect(self) -> List[Dict]:
        """
        Detect traffic spikes.

        Algorithm:
        - Calculate baseline: average packets per minute
        - Identify minutes where traffic > threshold * baseline
        - Generate alert for significant spikes
        """
        alerts = []

        # Get all packets ordered by timestamp
        packets = self.db.query(Packet).filter(
            Packet.session_id == self.session_id
        ).order_by(Packet.timestamp).all()

        if len(packets) < 100:  # Not enough data
            return alerts

        # Group packets by minute
        packets_per_minute = defaultdict(int)

        for packet in packets:
            # Round to minute
            minute = packet.timestamp.replace(second=0, microsecond=0)
            packets_per_minute[minute] += 1

        if not packets_per_minute:
            return alerts

        # Calculate baseline
        packet_counts = list(packets_per_minute.values())
        baseline = sum(packet_counts) / len(packet_counts)

        # Threshold for spike detection
        threshold = baseline * settings.TRAFFIC_SPIKE_MULTIPLIER

        # Detect spikes
        spike_minutes = []

        for minute, count in packets_per_minute.items():
            if count > threshold:
                spike_minutes.append((minute, count))

        # Generate alerts for significant spikes
        if spike_minutes:
            # Sort by packet count
            spike_minutes.sort(key=lambda x: x[1], reverse=True)

            # Report top spike
            top_minute, top_count = spike_minutes[0]

            alert = self.create_alert(
                alert_type="traffic_spike",
                severity="medium",
                title="Unusual Traffic Spike Detected",
                description=(
                    f"Traffic spike detected at {top_minute.strftime('%Y-%m-%d %H:%M')}. "
                    f"Observed {top_count} packets/minute, which is "
                    f"{(top_count / baseline):.1f}x the baseline average of {baseline:.0f} packets/minute."
                ),
                metadata=f'{{"spike_count": {top_count}, "baseline": {baseline:.2f}, "spike_minutes": {len(spike_minutes)}}}'
            )
            alerts.append(alert)

        return alerts
