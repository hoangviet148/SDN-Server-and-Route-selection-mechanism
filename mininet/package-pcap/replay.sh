CLIENT=$1
SERVER=$2
CLIENT_IP=$3
CLIENT_MAC=$4
SERVER_IP=$5
SERVER_MAC=$6

if [ -f "$CLIENT-$SERVER.pcap" ]; then
    tcpreplay --intf1="$CLIENT-eth0" $CLIENT-$SERVER.pcap
    exit 1
fi

tcprewrite --infile=log.pcap --outfile=temp1.pcap --srcipmap=0.0.0.0/0:$CLIENT_IP --enet-smac=$CLIENT_MAC 
tcprewrite --infile=temp1.pcap --outfile=temp2.pcap --dstipmap=0.0.0.0/0:$SERVER_IP --enet-dmac=$SERVER_MAC    
tcprewrite --infile=temp2.pcap --outfile="$CLIENT-$SERVER.pcap" --fixcsum
tcpreplay --intf1="$CLIENT-eth0" $CLIENT-$SERVER.pcap