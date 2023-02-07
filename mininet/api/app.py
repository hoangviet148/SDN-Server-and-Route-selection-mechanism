from flask import Flask, request, jsonify
import sys, json
import threading, logging, time

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/routingAlgorithm')
import DijkstraLearning, updateEndPointModel

sys.path.append(PATH_ABSOLUTE + '/run')
import generate_topo

import ccdn

sys.path.append(PATH_ABSOLUTE + '/cost-models')
import EndPointModel

sys.path.append(PATH_ABSOLUTE + '/dataPersist')
import LinkVersion

sys.path.append(PATH_ABSOLUTE + '/api/routes')
from ignore_ip_middleware import ignore_ip_middleware

from routes.sdn_controller_handler import sdn_controller_handler
from routes.predict import predict
from routes.write_full_data import write_full_data

# init
app = Flask(__name__)
# app.wsgi_app = ignore_ip_middleware(app.wsgi_app)
app.register_blueprint(sdn_controller_handler)
app.register_blueprint(predict)
app.register_blueprint(write_full_data)

# get full ip of SDN
list_ip = json.load(open(PATH_ABSOLUTE + '/setup/setup_topo.json'))["controllers"]

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

############################ CCDN ###############################
update_server = updateEndPointModel.updateEndPointModel(servers)
update_weight = ccdn.Update_weight_ccdn(topo=topo_network, update_server=update_server, list_ip=list_ip)

priority = 200
starttime = time.time()

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


@app.route('/read_link_version/',  methods=['GET', 'POST'])
def read_link_version():
    # API: get data from load send to CCDN when there is a request to read N_r SDNs
    if request.method == 'GET':
        data = LinkVersion.get_multiple_data()
        return jsonify({'link_versions': data})  # will return the json


# Lay BW
@app.route('/write_EndPoint/',  methods=['GET', 'POST'])
def write_EndPoint():
  if request.method == 'POST':
    content = request.data
    # print(json.loads(content)['EndPoint_datas'])
    end_point = json.loads(content)['EndPoint_datas']
    data_search = {
        'srcLink': end_point['srcLink'], 'portInfo': end_point['portInfo']}
    if EndPointModel.is_data_exit(end_point):
        EndPointModel.update_many(data_search, end_point)
    else:
        EndPointModel.insert_data(end_point)
    return content

# fix cung R, W
def ccdn():
    global starttime
    R = 4
    W = 0
    while True:
        if time.time() - starttime > 45:
            RD, WD, V_staleness = update_weight.load_CCDN(R, W)

            # cap nhap trong so cho server
            update_server.update_server_cost()
            starttime = time.time()

def flask_app():
    app.run(host='0.0.0.0', debug=True, use_reloader=False, threaded=True) 

if __name__ == '__main__':
    threading.Thread(target=flask_app).start()
    threading.Thread(target=ccdn).start()