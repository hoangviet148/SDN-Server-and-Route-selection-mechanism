from pymongo import MongoClient

mongo_uri = "mongodb://admin:admin@mongodb:27017/"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['Full_Data']
# print("Database connected")

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert_one(data)
    return

def insert_n_data(list_data):
    if len(list_data) == 0:
        return
    else:
        for data in list_data:
            print("===Full_Data insert_n_data data: ", data)
            if not collection.find_one(data): 
                collection.insert_one(data)


def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


# CLOSE DATABASE
# connection.close()

# weights = Model.find({})
# for w in weights:
#     print(w)
# insert one
# data = {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" }

# insert many
# data = [ {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" } ,
#         {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" }]
# weight_collection.insert(data)

# update one
# weight_collection.update({"dieukien", {"$set": {"gia tri sua"}}})
# weight_collection.update({"weight": "281"}, {"$set": {"src": "Son van dzai src"}})


# update many
# weight_collection.update_many({"weight": "281"}, {"$set": {"src": "Son van dzai src"}})

# delete
# weight_collection.delete_one({"Dieu kien"})
# weight_collection.delete_many({"Dieu kien"})