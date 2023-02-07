from flask import Blueprint, request
import sys, json
import requests

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
    print("Hit write_ccdn funtion")
    data = LinkVersion.get_multiple_data()
    url_ccdn = "http://" + ip_ccdn + ":5000/write_full_data"
    requests.post(url_ccdn, data=json.dumps({'link_versions': data}))
    return 

@sdn_controller_handler.route('/write_data', methods=['GET', 'POST'])
def write_data_funtion():
    if request.method == 'GET':
        return "Hit GET"

    if request.method == 'POST':
        print("Hit /write_data")
        content = request.data.decode()
        dicdata = {}
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
        check_overhead = (float(dicdata['byteSent']) + float(dicdata['byteReceived']))
        print("check_overhead", check_overhead)
        
        # if check_overhead > 15000000:
        if check_overhead > 500:
            print("****************** Cap nhat du lieu ******************")
            # push data to rabbit (mechanism pub/sub)
            # pub.connectRabbitMQ(data=dicdata)
            # consume data from rabbit
            # update.read_params_from_rabbit()
            # Update QoS parameter and save to local database   (using linkcost)
            update.write_update_link_to_data_base()

            try:
                # upload link learn to ccdn database
                write_ccdn()
            except:
                print("Error write to CCDN ~ MONGOD")
        return content 