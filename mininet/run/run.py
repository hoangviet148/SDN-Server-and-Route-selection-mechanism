import json
import time
import os

PATH_ABSOLUTE = "/app"

from mininet.net import Mininet
from mininet.node import RemoteController, Host, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import generate_topo

os.system("sudo mn -c")
set_up_topo = json.load(open(PATH_ABSOLUTE + '/setup/setup_topo.json'))
setLogLevel('debug')

controllers = [ c for c in set_up_topo['controllers'] ]
switches = [ sw for sw in set_up_topo['switches'] ]
hosts = [ sw for sw in set_up_topo['hosts'] ]
bridges = [ sw for sw in set_up_topo['bridges'] ]

net = Mininet( topo=None, build=False, controller=RemoteController)
for i in range(len(controllers)):
    controllers[i]['switches'] = [s for s in controllers[i]['switches']]

for i in range(len(switches)):
    switches[i]['hosts'] = [s for s in switches[i]['hosts']]
    switches[i]['name'] = switches[i]['name']

controllers_save = {}
switches_save = {} 
hosts_save = {}

info( '*** Adding controllers\n' )
for i in range(len(controllers)):
    controller_name = "c" + str(i)
    controller_net = net.addController(name=controller_name, ip=controllers[i]['ip'], protocol='tcp', port=controllers[i]['controller_port'])
    controllers_save[controller_name] = controller_net

# not_host = [ str(host).replace('s', 'h') for host in sum(set_up_topo['bridges'], []) ]
not_host = []

info( '*** Add switches\n')
for switch in switches:
    switch_net = net.addSwitch(switch['name'])
    switches_save[switch['name']] = switch_net

info( '*** Adding hosts\n' )
for host in hosts:
    if host['name'] not in not_host:
        ipv4 = "172.10.0." + str(int(host['name'].replace("h", "")))
        mac = host['mac']
        host_net = net.addHost(host['name'], mac=mac, ip=ipv4, defaultRoute=None)
        hosts_save[host['name']] = host_net

info( '*** Add links\n')
# add edge switch to switch
for bridge in bridges:
    net.addLink(switches_save[bridge[0]], switches_save[bridge[1]])
net.addLink("s3", "s6", port1=10, port2=10)

# add edge switch to host
print(switches)
for switch in switches:
    if switch['hosts']:
        print("=test=", switch)
        for host in switch['hosts']:
            net.addLink(switch['name'], host)

info( '*** Starting network\n' )
net.build()

info( '*** Starting controllers\n')
for key in controllers_save.keys():
    controllers_save[key].start()

map_switch_controller = {"c"+str(i): controllers[i]['switches'] for i in range(len(controllers))}

for key in controllers_save:
    for switch in map_switch_controller[key]:
        net.get(switch).start([controllers_save[key]])

net.pingAllFull()

generate_topo.generate_topo(net, hosts_save)
CLI(net)

net.stop()