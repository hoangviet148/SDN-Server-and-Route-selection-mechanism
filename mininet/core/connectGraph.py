import json
import ast

PATH_ABSOLUTE = ('/app')

class connectGraph(object):
    def __init__(self, file_topos, file_hosts):
        self.file_topos = file_topos
        self.file_hosts = file_hosts
        self.merge_topo()
        self.merge_host()

    def merge_topo(self):
        result_topo = {
            "devices": [],
            "links": []
        }

        for file in self.file_topos:
            try:
                with open(file) as handle:
                    object = json.loads(handle.read()).replace(': false', ':False').replace(': true', ':True')
                    object = ast.literal_eval(object)
                print("connectGraph - Read topo success")
            except:
                print("Read topo error!")
                raise

            devices = object['devices']
            links = object['links']

            # add links to Topo file
            for link in links:
                result_topo['links'].append(link)

            # add bridges to Topo file
            with open(PATH_ABSOLUTE + '/run/bridges.txt', 'r') as bridges:
                for bridge in bridges:
                    result_topo['links'].append(json.loads(bridge.rstrip()))

            # add switches to Topo file
            result_topo['devices'] = [ switch for switch in devices ]
            for switch in devices:
                result_topo['devices'].append(switch)

        # ghi ra file topo hop nhat mang
        file_topo_done = PATH_ABSOLUTE + '/topo.json'
        with open(file_topo_done, 'w') as output_file:
            json.dump(result_topo, output_file)

    def merge_host(self):
        result_host = {
            "hosts": []
        }
        # load host tu file
        for file in self.file_hosts:
            with open(file) as handle:
                object = json.loads(handle.read())
                object = "\'" + object + "\'"
                object = ast.literal_eval(object)
                object = json.loads(object)

            for host in object['hosts']:
                host_mac = str(host['mac'])
                try:
                    host_ip = str(host['ipAddresses'][0])
                except:
                    print("----------------------------------------rong host ip")

                locations = host['locations']
                location = locations[0]
                port = int(location['port'])
                device_id = str(location['elementId'])

                # cau
                bridges = open(PATH_ABSOLUTE + '/run/bridges.txt', 'r').readlines()
                list_bridges = [json.loads(host)['src']['device']
                                for host in bridges]

                # print(device_id)

                if str(device_id) in list_bridges:
                    print("XOA HOST ", host_ip, "TU THIET BI", device_id)
                    continue
                else:
                    # add host data to Host file
                    host_value = {
                        'port': port,
                        'mac': host_mac,
                        'deviceId': device_id,
                        'ipAddresses': host_ip
                    }
                    result_host['hosts'].append(host_value)

        # ghi ra file host cuoi cung
        file_host_done = PATH_ABSOLUTE + '/host.json'
        with open(file_host_done, 'w') as output_file:
            json.dump(result_host, output_file)