import subprocess as sb
import sys
import pika

QUEUE_NAME = 'tcp_package'
ROUTING_KEY = 'tcp_package'
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

cmd = 'tshark -i wlp0s20f3 -Y "tcp.payload" \
        -T fields \
        -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e ip.proto \
        -e _ws.col.Info -e tcp.payload \
        -E header=n -E separator=, -E quote=d -E occurrence=f \
        -a duration:30'


# cmd = 'tshark -i h1 -Y "gquic.payload" \
#         -T fields \
#         -e frame.time_epoch -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e ip.proto \
#         -e _ws.col.Info -e qgquic.payload \
#         -E header=n -E separator=, -E quote=d -E occurrence=f \
#         -a duration:30'

with open("packet-capture.log", "wb") as file:
    proc = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stdin=sb.PIPE)
    line = ''
    # lines = []
    for char in iter(lambda: proc.stdout.read(1), b''):
        file.write(char)
        if char == b'\n':
            channel.basic_publish(
                        exchange='',
                        routing_key=ROUTING_KEY,
                        body=line)
            # lines.append(line)
            # print(line)
            line = ''
            continue
        # print(char)
        line += char.decode('latin-1')
# print(lines[20])
connection.close()