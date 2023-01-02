import requests
import json
from requests.auth import HTTPBasicAuth

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

# Get topo from onos
def call_topo_api_sdn(list_ip):
    print("call_topo_api_sdn")
    for i in range(len(list_ip)):
        if list_ip[i]['controller'] == "onos":
            devices = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/devices', 
                auth=HTTPBasicAuth('onos', 'rocks')).content
            devicesDict = json.loads(devices)

            hosts = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/hosts', 
                auth=HTTPBasicAuth('onos', 'rocks')).content
            hostsDict = json.loads(hosts)

            links = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/links', 
                auth=HTTPBasicAuth('onos', 'rocks')).content
            linksDict = json.loads(links)

            response = {**devicesDict, **hostsDict, **linksDict}
            topos = json.dumps(response)

        with open('../topos/topo_'+str(i+1)+'.json', 'w') as f: json.dump(topos, f, cls=BytesEncoder)


def call_host_api_sdn(list_ip):
    print("call_host_api_sdn function")
    for i in range(len(list_ip)):
        if list_ip[i]['controller'] == "onos":
            response = requests.get('http://' + list_ip[i]['ip'] + ':8181/onos/v1/hosts',
                auth=HTTPBasicAuth('onos', 'rocks'))
        
        with open('../hosts/host_'+str(i+1)+'.json', 'w') as f: json.dump(response.content, f, cls=BytesEncoder)
    