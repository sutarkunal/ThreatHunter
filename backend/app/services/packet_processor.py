"""Packet processing service."""
import os
import logging
from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models import Session as SessionModel, Packet
from app.utils.pcap_parser import PCAPParser
from app.services.alert_manager import AlertManager
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class PacketProcessor:
    """Service for processing PCAP files and storing packets."""

    def __init__(self, db: Session):
        """
        Initialize packet processor.

        Args:
            db: Database session
        """
        self.db = db
        self.settings = settings

    async def process_pcap(self, session_id: int, file_path: str) -> Dict:
        """
        Process a PCAP file and store packets in the database.

        Args:
            session_id: Session ID
            file_path: Path to PCAP file

        Returns:
            Processing result dictionary
        """
        try:
            # Get session
            session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                raise ValueError(f"Session {session_id} not found")

            # Update session status
            session.status = "processing"
            self.db.commit()

            # Parse PCAP file
            logger.info(f"Parsing PCAP file: {file_path}")
            parser = PCAPParser(file_path)

            # Get capture info first
            capture_info = parser.get_capture_info()

            # Parse packets
            packets = parser.parse(max_packets=self.settings.MAX_PACKETS_PER_SESSION)

            logger.info(f"Parsed {len(packets)} packets")

            # Store packets in batches
            batch_size = self.settings.PACKET_PROCESSING_BATCH_SIZE
            unique_src_ips = set()
            unique_dst_ips = set()

            for i in range(0, len(packets), batch_size):
                batch = packets[i:i + batch_size]
                packet_objects = []

                for pkt_data in batch:
                    packet = Packet(
                        session_id=session_id,
                        timestamp=pkt_data['timestamp'],
                        src_ip=pkt_data['src_ip'],
                        dst_ip=pkt_data['dst_ip'],
                        src_port=pkt_data['src_port'],
                        dst_port=pkt_data['dst_port'],
                        protocol=pkt_data['protocol'],
                        length=pkt_data['length'],
                        flags=pkt_data['flags'],
                        info=pkt_data['info']
                    )
                    packet_objects.append(packet)

                    unique_src_ips.add(pkt_data['src_ip'])
                    unique_dst_ips.add(pkt_data['dst_ip'])

                # Bulk insert
                self.db.bulk_save_objects(packet_objects)
                self.db.commit()

                logger.info(f"Stored batch {i//batch_size + 1}")

            # Update session with statistics
            session.status = "completed"
            session.packet_count = len(packets)
            session.start_time = capture_info.get('start_time')
            session.end_time = capture_info.get('end_time')
            session.duration = capture_info.get('duration')
            session.unique_src_ips = len(unique_src_ips)
            session.unique_dst_ips = len(unique_dst_ips)
            self.db.commit()

            logger.info(f"Successfully processed session {session_id}")

            # Run threat detection
            logger.info(f"Running threat detection for session {session_id}")
            alert_manager = AlertManager(self.db)
            alert_count = alert_manager.run_threat_detection(session_id)
            logger.info(f"Generated {alert_count} alerts")

            return {
                'success': True,
                'session_id': session_id,
                'packets_processed': len(packets),
                'unique_src_ips': len(unique_src_ips),
                'unique_dst_ips': len(unique_dst_ips),
                'alerts_generated': alert_count
            }

        except Exception as e:
            logger.error(f"Error processing PCAP: {e}")

            # Update session status to failed
            session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if session:
                session.status = "failed"
                self.db.commit()

            return {
                'success': False,
                'error': str(e)
            }

    def get_packets(
        self,
        session_id: int,
        limit: int = 100,
        offset: int = 0,
        src_ip: str = None,
        dst_ip: str = None,
        protocol: str = None
    ) -> tuple[List[Packet], int]:
        """
        Query packets with filters.

        Args:
            session_id: Session ID
            limit: Maximum number of packets to return
            offset: Offset for pagination
            src_ip: Filter by source IP
            dst_ip: Filter by destination IP
            protocol: Filter by protocol

        Returns:
            Tuple of (packets list, total count)
        """
        query = self.db.query(Packet).filter(Packet.session_id == session_id)

        # Apply filters
        if src_ip:
            query = query.filter(Packet.src_ip == src_ip)
        if dst_ip:
            query = query.filter(Packet.dst_ip == dst_ip)
        if protocol:
            query = query.filter(Packet.protocol == protocol)

        # Get total count
        total = query.count()

        # Apply pagination
        packets = query.order_by(Packet.timestamp).offset(offset).limit(limit).all()

        return packets, total
