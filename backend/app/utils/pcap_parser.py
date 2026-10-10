"""PCAP parser utility using PyShark."""
import pyshark
from datetime import datetime
from typing import List, Dict, Optional
import logging
import asyncio
import nest_asyncio

# Allow nested event loops (required for PyShark in FastAPI)
nest_asyncio.apply()

logger = logging.getLogger(__name__)


class PCAPParser:
    """Parse PCAP files and extract packet information."""

    def __init__(self, file_path: str):
        """
        Initialize PCAP parser.

        Args:
            file_path: Path to the PCAP file
        """
        self.file_path = file_path
        self.capture = None

    def parse(self, max_packets: Optional[int] = None) -> List[Dict]:
        """
        Parse PCAP file and extract packet data.

        Args:
            max_packets: Maximum number of packets to parse (None for all)

        Returns:
            List of packet dictionaries
        """
        packets = []

        try:
            # Open PCAP file
            self.capture = pyshark.FileCapture(
                self.file_path,
                keep_packets=False  # Memory optimization
            )

            packet_count = 0

            for packet in self.capture:
                try:
                    packet_data = self._extract_packet_data(packet)
                    if packet_data:
                        packets.append(packet_data)
                        packet_count += 1

                        if max_packets and packet_count >= max_packets:
                            break

                except Exception as e:
                    logger.warning(f"Error parsing packet {packet_count}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error opening PCAP file: {e}")
            raise
        finally:
            if self.capture:
                self.capture.close()

        return packets

    def _extract_packet_data(self, packet) -> Optional[Dict]:
        """
        Extract relevant data from a packet.

        Args:
            packet: PyShark packet object

        Returns:
            Dictionary with packet information
        """
        try:
            # Get timestamp
            timestamp = datetime.fromtimestamp(float(packet.sniff_timestamp))

            # Get IP layer
            src_ip = None
            dst_ip = None

            if hasattr(packet, 'ip'):
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst
            elif hasattr(packet, 'ipv6'):
                src_ip = packet.ipv6.src
                dst_ip = packet.ipv6.dst
            else:
                # Skip non-IP packets
                return None

            # Get transport layer info
            src_port = None
            dst_port = None
            protocol = "Unknown"
            flags = None

            if hasattr(packet, 'tcp'):
                protocol = "TCP"
                src_port = int(packet.tcp.srcport)
                dst_port = int(packet.tcp.dstport)
                flags = packet.tcp.flags if hasattr(packet.tcp, 'flags') else None
            elif hasattr(packet, 'udp'):
                protocol = "UDP"
                src_port = int(packet.udp.srcport)
                dst_port = int(packet.udp.dstport)
            elif hasattr(packet, 'icmp'):
                protocol = "ICMP"
            elif hasattr(packet, 'icmpv6'):
                protocol = "ICMPv6"
            else:
                protocol = packet.highest_layer

            # Get packet length
            length = int(packet.length)

            # Get additional info
            info = packet.info if hasattr(packet, 'info') else str(packet.highest_layer)

            return {
                'timestamp': timestamp,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'protocol': protocol,
                'length': length,
                'flags': flags,
                'info': info[:500] if info else None  # Limit info length
            }

        except Exception as e:
            logger.warning(f"Error extracting packet data: {e}")
            return None

    def get_capture_info(self) -> Dict:
        """
        Get basic information about the PCAP file.

        Returns:
            Dictionary with capture metadata
        """
        try:
            capture = pyshark.FileCapture(self.file_path)

            # Get first and last packet timestamps
            first_packet = None
            last_packet = None
            packet_count = 0

            for packet in capture:
                packet_count += 1
                if first_packet is None:
                    first_packet = float(packet.sniff_timestamp)
                last_packet = float(packet.sniff_timestamp)

            capture.close()

            duration = None
            start_time = None
            end_time = None

            if first_packet and last_packet:
                start_time = datetime.fromtimestamp(first_packet)
                end_time = datetime.fromtimestamp(last_packet)
                duration = last_packet - first_packet

            return {
                'packet_count': packet_count,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration
            }

        except Exception as e:
            logger.error(f"Error getting capture info: {e}")
            return {
                'packet_count': 0,
                'start_time': None,
                'end_time': None,
                'duration': None
            }
