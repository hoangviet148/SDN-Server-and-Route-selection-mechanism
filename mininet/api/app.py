from flask import Flask, request, jsonify
import sys, json

PATH_ABSOLUTE = "../"

sys.path.append(PATH_ABSOLUTE + 'routingAlgorithm')
import DijkstraLearning

sys.path.append(PATH_ABSOLUTE + 'run')
import generate_topo

# init
app = Flask(__name__)

generate_topo_info = generate_topo.generate_topo_info()
topo_network = generate_topo_info.get_topo_from_api()
print(generate_topo_info)

# get host and server in topo
hosts = generate_topo_info.get_host_from_api()
servers = generate_topo_info.get_server_from_api()

priority = 200

@app.route('/getIpServer', methods=['POST'])
def get_ip_server():
    """
      input: ip_host
      output: ip_server
    """
    if request.method == 'POST':
        global priority
        global index_server
        priority += 10

        host_ip = request.data
        object = DijkstraLearning.hostServerConnection(topo_network, hosts, servers, priority)

        # pass src ip param and get dest ip
        object.set_host_ip(host_ip=str(host_ip))
        # update_server.update_server_cost()
        dest_ip = object.find_shortest_path()

        return str(dest_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)