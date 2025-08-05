import bson

def generate_object_id():
    return str(bson.ObjectId())