import setup_mininet
import json, os, time, random
import requests
import sys, json

PATH_ABSOLUTE = "../"

sys.path.append(PATH_ABSOLUTE + 'api')
import apiSDN

sys.path.append(PATH_ABSOLUTE + 'core')
import connectGraph, Graph

sys.path.append(PATH_ABSOLUTE + 'handleData/models')
import CustomTopo

class generate_topo_info:
    def __init__(self):
        self.list_ip = json.load(open('../setup/setup_topo.json'))["controllers"]
        self.topo_network  = ''
        self.hosts  = ''
        self.servers  = ''
        self.graph = ''

    def getApi(self):
        print("=== get api function ===")

        apiSDN.call_topo_api_sdn(self.list_ip)
        print("finished read topo")

        apiSDN.call_host_api_sdn(self.list_ip)
        print("finished read host")

        number_ip = len(self.list_ip) + 1
        topo_files = [PATH_ABSOLUTE + 'topos/topo_' + str(index_path) + '.json' for index_path in range(1, number_ip)]
        host_files = [PATH_ABSOLUTE + 'hosts/host_' + str(index_path) + '.json' for index_path in range(1, number_ip)]

        # connectGraph
        connectGraph.connectGraph(topo_files, host_files)

        # init empty topo
        self.topo_network = CustomTopo.Topo()
        # add graph topo.json va host.json to topo
        self.graph = Graph.Graph(self.topo_network, '../topo.json', '../host.json')

        # get list hosts va servers in topo
        self.hosts  = self.topo_network.get_hosts()
        self.servers = self.topo_network.get_servers()

        name_hosts = [ip_host.replace('172.10.0.', 'h') for ip_host in self.hosts.keys()]
        name_servers = [ip_server.replace('172.10.0.', 'h') for ip_server in self.servers.keys()]

        return name_hosts, name_servers
    
    def get_topo_from_api(self):
        return self.topo_network

    def get_graph_from_api(self):
        return self.graph

    def get_host_from_api(self):
        return self.hosts

    def get_server_from_api(self):
        return self.servers

def generate_topo(net, hosts_save):
    print("=== generate_topo ===")
    gtopo = generate_topo_info()
    name_hosts, name_servers = gtopo.getApi()

    print(name_hosts, name_servers)
    print(hosts_save)

    server_list = [ hosts_save[h] for h in  name_servers ]
    print(server_list)

    name_host = name_hosts
    run_shedule()

def run_shedule(generate_flow, net, life_time):
    print("generate_flow--------")
    des = call_routing_api_flask( p.IP() )

def call_routing_api_flask(host):
    print("call flask")
    response = requests.post("http://flask:5000/getIpServer", data=host)  
    dest_ip = response.text
    return str(dest_ip)