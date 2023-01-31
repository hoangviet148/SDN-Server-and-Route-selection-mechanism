from scapy.all import *

input_pcap_file="./FileTransfer/FileTransfer_00001_20180328094056.pcap"
output_pcap_file="temp.pcap"
old_source_mac_1="b0:83:fe:59:14:ca"
new_source_mac_1="00:00:00:01:01:21"
old_destination_mac_1="60:02:92:21:4c:d2"
new_destination_mac_1="00:00:00:02:05:24"

packets = rdpcap(input_pcap_file)
for packet in packets:
    if packet.src == old_source_mac_1:
        packet.src = new_source_mac_1
    if packet.dst == old_destination_mac_1:
        packet.dst = new_destination_mac_1
wrpcap(output_pcap_file, packets)


old_source_mac_2="60:02:92:21:4c:d2"
new_source_mac_2="00:00:00:02:05:24"
old_destination_mac_2="b0:83:fe:59:14:ca"
new_destination_mac_2="00:00:00:01:01:21"

packets = rdpcap(output_pcap_file)
for packet in packets:
    if packet.src == old_source_mac_2:
        packet.src = new_source_mac_2
    if packet.dst == old_destination_mac_2:
        packet.dst = new_destination_mac_2
wrpcap(output_pcap_file, packets)


# rewrite src ip
packets = rdpcap(output_pcap_file)
src_ip_pairs = [
    ("192.168.10.30", "172.10.0.21"),
    ("192.168.10.35", "172.10.10.24"),
]

# Iterate over each packet
for packet in packets:
    # Iterate over the IP address pairs
    for old_src, new_src in src_ip_pairs:
        # Check if the current packet's IP addresses match the current IP address pair
        if packet[IP].src == old_src:
            # Change the source and destination IP addresses
            packet[IP].src = new_src
            break

# Save the modified packets to a new PCAP file
wrpcap(output_pcap_file, packets)


# rewrite dst ip
packets = rdpcap(output_pcap_file)
dst_ip_pairs = [
    ("192.168.10.30", "172.10.0.21"),
    ("192.168.10.35", "172.10.10.24"),
]

# Iterate over each packet
for packet in packets:
    # Iterate over the IP address pairs
    for old_dst, new_dst in src_ip_pairs:
        # Check if the current packet's IP addresses match the current IP address pair
        if packet[IP].dst == old_dst:
            # Change the source and destination IP addresses
            packet[IP].dst = new_dst
            break

# Save the modified packets to a new PCAP file
wrpcap(output_pcap_file, packets)