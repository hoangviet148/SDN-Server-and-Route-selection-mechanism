from json import encoder
from flask import Blueprint, request
import sys, json

PATH_ABSOLUTE = "/app"

sys.path.append(PATH_ABSOLUTE + '/cost-models')
import Full_Data

write_full_data = Blueprint('write_full_data', __name__)

def deunicodify_hook(pairs):
    print("Hit deunicodify_hook")
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)

@write_full_data.route('/write_full_data', methods=['POST'])
def write_full_data_funtion():
  if request.method == 'POST':
    print("Hit /write_full_data")
    content = request.data
    # data = json.loads(content, object_pairs_hook=deunicodify_hook)
    data = json.loads(content)
    # del data["_id"]
    Full_Data.insert_n_data([data['link_versions']])
    # print(data)
    return content