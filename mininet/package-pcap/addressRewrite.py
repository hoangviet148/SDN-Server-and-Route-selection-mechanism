from scapy.all import *
import sys

CLIENT = "h21"
CLIENT_IP = ""
CLIENT_MAC = ""

SERVER = "h24"
SERVER_IP = ""
SERVER_MAC = ""

input_pcap_file = "./FileTransfer/FileTransfer_00001_20180328094056.pcap"
output_pcap_file = "%s-%s.pcap" % (CLIENT, SERVER)

pairs = [
    {
        "old_ip": "192.168.10.30",
        "old_mac": "b0:83:fe:59:14:ca",
        "new_ip": CLIENT_IP,
        "new_mac": CLIENT_MAC
    },
    {
        "old_ip": "192.168.10.35",
        "old_mac": "60:02:92:21:4c:d2",
        "new_ip": SERVER_IP,
        "new_mac": SERVER_MAC
    },
]

packets = rdpcap(input_pcap_file)
for packet in packets:
    for item in pairs:
        # Check if the current packet's MAC addresses match the current MAC address pair
        if packet.src == item["old_mac"]:
            print("==test 1==")
            # Change the source MAC addresses
            packet.src = item["new_mac"]
        if packet.dst == item["old_mac"]:
            print("==test 2==")
            # Change the destination MAC addresses
            packet.dst = item["new_mac"]
    
        # Check if the current packet's IP addresses match the current IP address pair
        if packet[IP].src == item["old_ip"]:
            print("==test 3==")
            # Change the source IP addresses
            packet[IP].src = item["new_ip"]
        if packet[IP].dst == item["old_ip"]:
            print("==test 4==")
            # Change the destination IP addresses
            packet[IP].dst = item["new_ip"]
wrpcap(output_pcap_file, packets)
