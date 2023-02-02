CLIENT=$1
SERVER=$2
CLIENT_IP=$3
CLIENT_MAC=$4
SERVER_IP=$5
SERVER_MAC=$6

if [ -f "$CLIENT-$SERVER.pcap" ]; then
    echo "==== start replay ===="
    tcpreplay --intf1="$CLIENT-eth0" $CLIENT-$SERVER.pcap
    exit 1
fi
 
python3 addressRewrite.py $CLIENT $SERVER $CLIENT_IP $CLIENT_MAC $SERVER_IP $SERVER_MAC
echo "==== start replay ===="
tcpreplay --intf1="$CLIENT-eth0" $CLIENT-$SERVER.pcap