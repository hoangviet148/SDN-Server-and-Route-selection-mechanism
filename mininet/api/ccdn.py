import sys
import time

class Update_weight_ccdn(object):
    def __init__(self, topo, update_server, list_ip):
        self.LinkVersions = ""
        self.count = 0
        self.topo = topo
        self.update_server = update_server
        self.list_ip = list_ip
        self.q_table = q_table.Q_table()
        self.time_run = 60*60*5 # 60ph
        self.start_run = time.time()