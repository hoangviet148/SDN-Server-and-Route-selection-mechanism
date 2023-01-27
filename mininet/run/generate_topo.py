import setup_mininet
import json, os, time, random
import requests
import sys, json

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/api')
import apiSDN

sys.path.append(PATH_ABSOLUTE + '/core')
import connectGraph, Graph

sys.path.append(PATH_ABSOLUTE + '/handleData/models')
import CustomTopo

class generate_topo_info:
    def __init__(self):
        self.list_ip = json.load(open(PATH_ABSOLUTE + '/setup/setup_topo.json'))["controllers"]
        self.topo_network  = ''
        self.hosts  = ''
        self.servers  = ''
        self.graph = ''

    def getApi(self):
        print("=== get api function ===")

        apiSDN.call_topo_api_sdn(self.list_ip)
        print("finished read topo")

        number_ip = len(self.list_ip) + 1
        topo_files = [PATH_ABSOLUTE + '/topos/topo_' + str(index_path) + '.json' for index_path in range(1, number_ip)]
        host_files = [PATH_ABSOLUTE + '/hosts/host_' + str(index_path) + '.json' for index_path in range(1, number_ip)]

        # connectGraph
        connectGraph.connectGraph(topo_files, host_files)

        # init empty topo
        self.topo_network = CustomTopo.Topo()
        # add graph topo.json va host.json to topo
        self.graph = Graph.Graph(self.topo_network, PATH_ABSOLUTE + '/topo.json', PATH_ABSOLUTE + '/host.json')

        # get list hosts va servers in topo
        self.hosts  = self.topo_network.get_hosts()
        self.servers = self.topo_network.get_servers()

        name_hosts = [ip_host.replace('172.10.0.', 'h') for ip_host in self.hosts.keys()]
        name_servers = [ip_server.replace('172.10.0.', 'h') for ip_server in self.servers.keys()]

        print("=== name_hosts ===", name_hosts)
        print("=== name_servers ===", name_servers)

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

    print("name_hosts, name_servers", name_hosts, name_servers)
    print(hosts_save)

    server_list = [ hosts_save[h] for h in  name_servers ]
    print(server_list)

    name_host = name_hosts

    period = setup_mininet.PERIOD # random data from 0 to period 
    interval = setup_mininet.INTERVAL # each host generates data 5 times randomly
    life_time = setup_mininet.LIFE_TIME

    # khoi tao bang thoi gian cho tung host
    starting_table = create_starting_table(name_host, period, interval, life_time)
    write_table_to_file(starting_table, 'starting_table.json')

    run_shedule(starting_table, net, life_time)

def run_shedule(generate_flow, net, life_time):
    print("generate_flow--------")
    p = net.get('h21')
    des = call_routing_api_flask( p.IP() )

def call_routing_api_flask(host):
    print("call_routing_api_flask", host)
    response = requests.post("http://172.10.0.14:5000/getIpServer", data=host)  
    dest_ip = response.text
    return str(dest_ip)

def create_starting_table(host_list, period, interval, life_time):
    generate_flow = {}
    # generate_flow = {0: {'h2': 569, 'h1': 441}, 1: {'h2': 358, 'h1': 366}, 2: {'h2': 302, 'h1': 315}}
    for i in range(interval):
        temp = {}
        if i == 0:
            time_f = random.sample(range(3, period), len(host_list))
            for j in range(len(host_list)):
                temp[host_list[j]] = time_f[j]
        else:
            for h_i in host_list:
                temp[h_i] =  generate_flow[i-1][h_i] + life_time + random.randint(0, 3)
        generate_flow[i] = temp
    return generate_flow

def write_table_to_file(table, name_file):
    with open(name_file, "w") as outfile:
        json.dump(table, outfile)