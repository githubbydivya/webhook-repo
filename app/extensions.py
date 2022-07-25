import certifi
import pymongo


# Setup MongoDB here
class MongoConnection:
    conn = None

    def connect(self):
        client = pymongo.MongoClient(
            "mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER_URL}/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        mydb = client.test
        return mydb

