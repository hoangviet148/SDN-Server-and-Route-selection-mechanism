from flask import Blueprint, request
import sys
import json
import requests
import random

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/linkTopo')
import updateWeight

sys.path.append(PATH_ABSOLUTE + '/dataPersist')
import LinkVersion

sdn_controller_handler = Blueprint('sdn_controller_handler', __name__)

ip_ccdn = str(json.load(open(PATH_ABSOLUTE + '/config.json'))['ip_ccdn'])
update = updateWeight.updateWeight()


def write_ccdn():
    # Get data from local and upload to ccdn database
    print("Hit write_full_data write_ccdn funtion")
    data = LinkVersion.get_multiple_data()
    url_ccdn = "http://" + ip_ccdn + ":5000/write_full_data"
    requests.post(url_ccdn, data=json.dumps({'link_versions': data}))
    return


def write_update_link_to_data_base(dicdata):
    print("=== sdn-controller-handler dicdata: ", dicdata)

    linkUtilization = dicdata['linkUtilization'] if dicdata['linkUtilization'] == 1.0 else random.uniform(
        0, 0.7)
    packet_loss = dicdata['packetLossRate'] if dicdata['packetLossRate'] == 1.0 and dicdata['packetLossRate'] == 0.0 else random.uniform(
        0.02, 0.26)
    byte_sent = float(dicdata['byteSent'])
    byte_received = float(dicdata['byteReceived'])
    overhead = abs((byte_sent + byte_received)) / 1000000 + 10  # convert to MB

    temp_data = {
        "src": dicdata['src'],
        "dst": dicdata['dst'],
        "delay": float(dicdata['delay']),
        "linkUtilization": float(linkUtilization),
        "packetLoss": float(packet_loss),
        "IpSDN": dicdata['IpSDN'],
        "overhead": float(overhead),
        "byteSent": float(byte_sent),
        "byteReceived": float(byte_received)
    }
    try:
        data_search = {'src': temp_data['src'], 'dst': temp_data['dst']}
        print("INSERT LINK VERSION")
        if LinkVersion.is_data_exit(data_search=data_search):
            # temp_data['linkVersion'] = data_search['linkVersion'] + 1
            LinkVersion.update_many(data_search, temp_data)
            print("Update LinkVersion success")
        else:
            LinkVersion.insert_data(data=temp_data)
            print("Insert LinkVersion success")
    except Exception as e:
        print("=== Write LinkVersion fail", e)


@sdn_controller_handler.route('/write_data', methods=['GET', 'POST'])
def write_data_funtion():
    if request.method == 'GET':
        return "Hit GET"

    if request.method == 'POST':
        print("Hit /write_data")
        content = request.data.decode()
        src_ip = request.remote_addr
        dicdata = {}
        dicdata['IpSDN'] = src_ip
        datas = content.split("&")

        # processing data
        for data in datas:
            d = data.split(":")
            if len(d) == 3:
                temp = [d[1], d[2]]
                dicdata[d[0]] = ":".join(temp)
            else:
                dicdata[d[0]] = d[1]
        #  remove default data
        check_overhead = (
            float(dicdata['byteSent']) + float(dicdata['byteReceived']))
        print("check_overhead", check_overhead)

        # if check_overhead > 15000000:
        if check_overhead > 500:
            print("****************** Update graph weight ******************")
            write_update_link_to_data_base(dicdata)

            # try:
            #     write_ccdn()
            # except:
            #     print("Error write to CCDN ~ MONGOD")
        return content
