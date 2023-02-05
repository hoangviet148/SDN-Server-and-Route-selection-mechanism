from scapy.all import rdpcap

pcap_file = "./VoIP/VoIP.pcap"
packets = rdpcap(pcap_file)

src_ips = set()
dst_ips = set()

for packet in packets:
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_ips.add(src_ip)
    dst_ips.add(dst_ip)

print(src_ips)
print(dst_ips)