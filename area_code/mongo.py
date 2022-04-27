from area_code import settings
import pymongo


class MongoClient(object):

    def __init__(self):
        self.host = settings.MONGO_HOST
        self.port = settings.MONGO_PORT
        self.user = settings.MONGO_USER
        self.password = settings.MONGO_PASS
        uri = "mongodb://%s:%s@%s:%s" % (
            self.user,
            self.password,
            self.host,
            self.port
        )
        client = pymongo.MongoClient(uri)
        self.db = client[settings.MONGO_DB]

    def get_collection(self, collection):
        return self.db[collection]


