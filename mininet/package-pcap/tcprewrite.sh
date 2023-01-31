CLIENT=$1
SERVER=$2
CLIENT_IP=$3
CLIENT_MAC=$4
SERVER_IP=$5
SERVER_MAC=$6

ORIGIN_PCAP="./FileTransfer/FileTransfer_00001_20180328094056.pcap"

if [ -f "$CLIENT_$SERVER.pcap" ]; then
    tcpreplay --intf1="$CLIENT-eth0" $CLIENT-$SERVER.pcap
    exit 1
fi

tcprewrite --infile=$ORIGIN_PCAP --outfile="temp.pcap" --enet-smacmap=60:02:92:21:4c:d2,$CLIENT_MAC
# tcprewrite --infile="temp.pcap" --outfile="temp.pcap" --enet-smac=$SERVER_MAC --enet-dmac=$CLIENT_MAC --srcipmap=192.168.10.35:172.10.0.24 --dstipmap=192.168.10.30:172.10.0.21

# tcprewrite --infile=$ORIGIN_PCAP --outfile="temp.pcap" --enet-smac=192.168.10.30,$CLIENT_MAC
# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="temp.pcap" --endpoints=192.168.10.35:192.168.10.30 --enet-smac="60:02:92:21:4c:d2,$SERVER_MAC"

# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="temp.pcap" --endpoints=192.168.10.30:192.168.10.35 --srcipmap="192.168.10.30:$CLIENT_IP" 
# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="temp.pcap" --endpoints=192.168.10.35:192.168.10.30 --srcipmap="192.168.10.35:$SERVER_IP"

# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="temp.pcap" --endpoints=192.168.10.30:192.168.10.35 --dstipmap="192.168.10.30:$CLIENT_IP"
# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="temp.pcap" --endpoints=192.168.10.35:192.168.10.30 --dstipmap="192.168.10.35:$SERVER_IP"

# tcprewrite --cachefile=in.cache --infile="temp.pcap" --outfile="$CLIENT_$SERVER.pcap" --fixcsum
# tcpreplay --intf1="$CLIENT-eth0" "$CLIENT_$SERVER.pcap"