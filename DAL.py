import pymongo


class Database(object):
    URI = 'mongodb+srv://stenzil:woodfelder@tb.jqlktc8.mongodb.net/TwitterBlack?retryWrites=true&w=majority'
    db = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.db = client['TwitterBlack']

    @staticmethod
    def find(collection, query):
        Database.db[collection].find(query)

    @staticmethod
    def findso(collection, query, so):
        Database.db[collection].find(query).sort(so)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert_one(data)
