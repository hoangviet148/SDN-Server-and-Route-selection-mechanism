import sys
import time
import json
from numpy import NaN, average
import requests
import random
import numpy as np

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/routingAlgorithm')
import updateLinkTopo

class Update_weight_ccdn(object):
    def __init__(self, topo, update_server, list_ip):
        self.LinkVersions = ""
        self.count = 0
        self.topo = topo
        self.update_server = update_server
        self.list_ip = list_ip
        self.time_run = 60*60*5 # 60ph
        self.start_run = time.time()
        
    def calculate_avg_overhead(self, link_versions):
        overheads = [version['overhead'] for version in link_versions]
        # if overheads empty
        if not overheads:
            return 0
        else: 
            return np.mean(overheads)

    def read_SDN(self):
        link_versions = []
        print("=== ccdn read_SDN list_ip", self.list_ip)
        try:
            url = "http://" + 'flask' + ":5000/read_link_version/"
            response = requests.get(url)
            link_object = json.loads(response.text)
            link_versions.extend(link_object['link_versions'])
        except Exception as e:
            print("Call API read_link_version error", e)
        return link_versions
    
    def write_SDN(self):
        list_time_write = []
        # time_start_write = time.time()
        try:
            url = "http://" + 'flask' + ":5000/write_SDN/"
            repo = requests.post(url, data=str(W))
        except:
            print("GOI API W LOI")
        # list_time_write.append( time.time() - time_start_write )
        # time_start_write = time.time()
        return int(average(list_time_write) * 1000)
        
    def load_ccdn(self):
        # write_delay = self.write_SDN()
        link_versions = self.read_SDN()
        self.calculate_link_weight(link_versions)
        return

    def calculate_link_weight(self, link_versions):
        print('Tinh trong so')
        link_weight = updateLinkTopo.updateLinkTopo(link_verions= link_versions)
        link_weight.get_link_weight()
        self.topo.read_update_weight()

        