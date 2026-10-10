"""
Simple script to generate test PCAP files with various traffic patterns.
This helps test ThreatHunter's detection capabilities.

Requirements:
    pip install scapy

Usage:
    python generate_test_pcap.py
"""
from scapy.all import IP, TCP, UDP, ICMP, wrpcap, Ether
from datetime import datetime
import random

def generate_normal_traffic(count=100):
    """Generate normal HTTP/HTTPS traffic."""
    packets = []
    src_ips = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
    dst_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]

    for _ in range(count):
        src_ip = random.choice(src_ips)
        dst_ip = random.choice(dst_ips)
        src_port = random.randint(49152, 65535)
        dst_port = random.choice([80, 443])

        pkt = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S")
        packets.append(pkt)

    return packets

def generate_port_scan(src_ip="192.168.1.100", dst_ip="10.0.0.50", port_count=60):
    """Generate port scan traffic (should trigger alert)."""
    packets = []

    for port in range(1, port_count + 1):
        pkt = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=54321, dport=port, flags="S")
        packets.append(pkt)

    return packets

def generate_suspicious_port_traffic():
    """Generate traffic to suspicious ports (should trigger alert)."""
    packets = []
    suspicious_ports = [21, 23, 445, 3389, 1433, 3306]
    src_ip = "192.168.1.200"
    dst_ip = "10.0.0.100"

    for port in suspicious_ports:
        for _ in range(5):
            pkt = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=random.randint(49152, 65535), dport=port, flags="S")
            packets.append(pkt)

    return packets

def generate_excessive_requests(src_ip="192.168.1.150", count=200):
    """Generate excessive requests from single IP (should trigger alert)."""
    packets = []
    dst_ip = "10.0.0.200"

    for _ in range(count):
        pkt = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=random.randint(49152, 65535), dport=80, flags="S")
        packets.append(pkt)

    return packets

def generate_icmp_traffic(count=50):
    """Generate ICMP ping traffic."""
    packets = []
    src_ips = ["192.168.1.10", "192.168.1.11"]
    dst_ips = ["8.8.8.8", "1.1.1.1"]

    for _ in range(count):
        src_ip = random.choice(src_ips)
        dst_ip = random.choice(dst_ips)
        pkt = Ether() / IP(src=src_ip, dst=dst_ip) / ICMP()
        packets.append(pkt)

    return packets

def main():
    """Generate test PCAP files."""

    print("Generating test PCAP files...")

    # 1. Normal traffic PCAP
    print("\n1. Generating normal_traffic.pcap...")
    normal_packets = generate_normal_traffic(100)
    normal_packets += generate_icmp_traffic(20)
    wrpcap("normal_traffic.pcap", normal_packets)
    print(f"   Created with {len(normal_packets)} packets")

    # 2. Port scan PCAP (should trigger alert)
    print("\n2. Generating port_scan_attack.pcap...")
    port_scan_packets = generate_normal_traffic(50)
    port_scan_packets += generate_port_scan(port_count=60)
    port_scan_packets += generate_normal_traffic(50)
    wrpcap("port_scan_attack.pcap", port_scan_packets)
    print(f"   Created with {len(port_scan_packets)} packets")
    print("   ⚠️  Should trigger: Port Scan Detection (HIGH)")

    # 3. Suspicious ports PCAP (should trigger alert)
    print("\n3. Generating suspicious_ports.pcap...")
    suspicious_packets = generate_normal_traffic(30)
    suspicious_packets += generate_suspicious_port_traffic()
    suspicious_packets += generate_normal_traffic(30)
    wrpcap("suspicious_ports.pcap", suspicious_packets)
    print(f"   Created with {len(suspicious_packets)} packets")
    print("   ⚠️  Should trigger: Suspicious Port Detection (HIGH/MEDIUM)")

    # 4. Excessive requests PCAP (should trigger alert)
    print("\n4. Generating excessive_requests.pcap...")
    excessive_packets = generate_normal_traffic(50)
    excessive_packets += generate_excessive_requests(count=200)
    excessive_packets += generate_normal_traffic(50)
    wrpcap("excessive_requests.pcap", excessive_packets)
    print(f"   Created with {len(excessive_packets)} packets")
    print("   ⚠️  Should trigger: Excessive Requests Detection (MEDIUM)")

    # 5. Multiple threats PCAP (should trigger multiple alerts)
    print("\n5. Generating multiple_threats.pcap...")
    multi_packets = generate_normal_traffic(100)
    multi_packets += generate_port_scan(port_count=30)
    multi_packets += generate_suspicious_port_traffic()
    multi_packets += generate_excessive_requests(count=150)
    multi_packets += generate_normal_traffic(100)
    wrpcap("multiple_threats.pcap", multi_packets)
    print(f"   Created with {len(multi_packets)} packets")
    print("   ⚠️  Should trigger: Multiple alerts")

    print("\n✅ All test PCAP files generated successfully!")
    print("\nGenerated files:")
    print("  - normal_traffic.pcap (baseline)")
    print("  - port_scan_attack.pcap")
    print("  - suspicious_ports.pcap")
    print("  - excessive_requests.pcap")
    print("  - multiple_threats.pcap")
    print("\nUpload these files to ThreatHunter to test threat detection!")

if __name__ == "__main__":
    main()
