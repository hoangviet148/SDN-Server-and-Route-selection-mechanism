from scapy.all import *
import sys
import subprocess

CLIENT = sys.argv[1]
SERVER = sys.argv[2]

CLIENT_IP = sys.argv[3]
CLIENT_MAC = sys.argv[4]

SERVER_IP = sys.argv[5]
SERVER_MAC = sys.argv[6]

SERVICE_NAME = sys.argv[7]

input_pcap_file = "./%s/%s.pcap" % (SERVICE_NAME, SERVICE_NAME)
output_pcap_file = "%s-%s-%s.pcap" % (CLIENT, SERVER, SERVICE_NAME)

def replay():
    print("start replay")
    command = f"""
    tcpreplay --intf1='{CLIENT}-eth0' {output_pcap_file}
    """
    subprocess.run(["bash", "-c", command], capture_output=True, text=True)
    print("End replay")

if os.path.exists(output_pcap_file):
    print("already rewrite")
    replay()

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

print("Start rewrite ip")
packets = rdpcap(input_pcap_file)
for packet in packets:
    for item in pairs:
        # Check if the current packet's MAC addresses match the current MAC address pair
        if packet.src == item["old_mac"]:
            # Change the source MAC addresses
            packet.src = item["new_mac"]
        if packet.dst == item["old_mac"]:
            # Change the destination MAC addresses
            packet.dst = item["new_mac"]
    
        # Check if the current packet's IP addresses match the current IP address pair
        if packet[IP].src == item["old_ip"]:
            # Change the source IP addresses
            packet[IP].src = item["new_ip"]
        if packet[IP].dst == item["old_ip"]:
            # Change the destination IP addresses
            packet[IP].dst = item["new_ip"]
wrpcap(output_pcap_file, packets)
print("End rewrite ip")

replay()