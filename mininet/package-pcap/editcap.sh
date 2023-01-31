#!/bin/bash

input_pcap_file="./FileTransfer/FileTransfer_00001_20180328094056.pcap"
output_pcap_file="temp.pcap"
old_source_mac="b0:83:fe:59:14:ca"
new_source_mac="00:00:00:01:02:23"
old_destination_mac="60:02:92:21:4c:d2"
new_destination_mac="00:00:00:02:05:24"

editcap -F libpcap -s $old_source_mac "$new_source_mac" -d "$old_destination_mac" "$new_destination_mac" "$input_pcap_file" "$output_pcap_file"
