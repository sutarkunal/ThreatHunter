"""Create a very simple test PCAP file"""
from scapy.all import IP, TCP, UDP, ICMP, wrpcap, Ether
import random

print("Creating simple test PCAP...")

packets = []

# Add 100 simple HTTP packets
for i in range(100):
    pkt = Ether()/IP(src="192.168.1.10", dst="8.8.8.8")/TCP(sport=50000+i, dport=80, flags="S")
    packets.append(pkt)

# Add 50 DNS packets
for i in range(50):
    pkt = Ether()/IP(src="192.168.1.10", dst="8.8.8.8")/UDP(sport=50000+i, dport=53)
    packets.append(pkt)

# Add some ICMP
for i in range(20):
    pkt = Ether()/IP(src="192.168.1.10", dst="8.8.8.8")/ICMP()
    packets.append(pkt)

wrpcap("simple_test.pcap", packets)
print(f"Created simple_test.pcap with {len(packets)} packets")
print("Upload this file to ThreatHunter!")
