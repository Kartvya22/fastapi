from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017/test"

client = MongoClient(uri)

db = client.test

user_collection = db["Users"]
sample_collection = db['Samples']