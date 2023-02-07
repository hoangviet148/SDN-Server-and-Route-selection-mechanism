from pymongo import MongoClient

mongo_uri = "mongodb://admin:admin@mongodb:27017"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['LinkVersion']

try:
    info = connection.server_info()
    print("Connected to MongoDB version", info['version'])
except Exception as e:
    print("Could not connect to MongoDB:", e)

def is_data_exit(data_search):
    return collection.count_documents({ 'src': data_search['src'] , 'dst': data_search['dst'] }, limit = 1)

def update_many(data_search, data_update):
    collection.update_many(data_search, {'$set':data_update})
    return

def insert_n_data(list_data):
    if len(list_data) == 0:
        return
    else:
        collection.insert_many(list_data)

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert(data)
    return

def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    print("Hit get_multiple_data funtion")
    data = collection.find({}, {'_id': 0})
    try:
        print("data", list(data))
    except Exception as e:
        print("==== error at get_multiple_data function ====", e)
    return list(data)

def remove_all():
    """
    remove all documents in collection
    :return:
    """
    collection.remove({})
    return

# CLOSE DATABASE
# connection.close() 