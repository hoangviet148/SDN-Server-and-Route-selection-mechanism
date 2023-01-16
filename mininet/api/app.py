from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import sys, json
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/routingAlgorithm')
import DijkstraLearning

sys.path.append(PATH_ABSOLUTE + '/run')
import generate_topo

import ccdn

# init
app = Flask(__name__)

generate_topo_info = generate_topo.generate_topo_info()
generate_topo_info.getApi()
topo_network = generate_topo_info.get_topo_from_api()

topo_network = generate_topo_info.get_topo_from_api()
# add do thi topo.json va host.json vao topo
graph = generate_topo_info.get_graph_from_api()

# get host and server in topo
hosts = generate_topo_info.get_host_from_api()
servers = generate_topo_info.get_server_from_api()
print("HOSTS: ", hosts)
print("SERVER: ", servers)

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
        object.set_host_ip(host_ip=str(host_ip, "utf-8"))
        # update_server.update_server_cost()
        dest_ip = object.find_shortest_path()
        print(dest_ip)
        return str(dest_ip)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        request_data = request.get_json()
        x_test = request_data["flow"]

        model = tf.keras.models.load_model(PATH_ABSOLUTE + "/api/model/model.h5")

        predictions_1flow = model.predict(x_test)
        one_flow_pred = int(np.argmax(predictions_1flow, axis=-1))

        return str(one_flow_pred)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)