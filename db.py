
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DB():

    def __init__(self):
        self.uri = "mongodb+srv://kevin199932:nr0UHZ4eZ998u3yN@pixage.1ml6xhf.mongodb.net/?retryWrites=true&w=majority&appName=pixage"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.client['Pixage']
        

    # Create a new client and connect to the server
    # Send a ping to confirm a successful connection
    def insert(self, document, db_name):
        try:
            self.collection = self.database[db_name]

            # collection.create_index('url', unique=True)
            self.collection.insert_one(document)
            # for c in collection.find({}):
            #     print(c)
            # client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        self.client.close()
        print("Connection closed")

    def find(self, filter, db_name):
        self.collection = self.database[db_name]
        return self.collection.find(filter)

    def delAll(self):
        self.collection.delete_many({})
        print("Successfully deleted every documents")
    
    def pickRandom(self, filter, db_name):
        self.collection = self.database[db_name]
        return list(self.collection.aggregate(filter))
    
    def update(self, filter, update, db_name):
        self.collection = self.database[db_name]
        self.collection.update_many(filter, update, upsert = True)


def main():

    db = DB()

    # db.delAll()

    db.update({}, {"$set": {"tag": "blue archive"}})


    # filter = [
    #         {"$match": {"r18": True}},
    #         {'$sample': {"size": 1}}
    #     ]
    # print(db.pickRandom(filter))
    # for c in db.pickRandom(filter):
    #     print(c)

    # doc = {"r18": True, "url": "byedbye"}
    # db.insert(doc)
    # db.close()

if __name__ == "__main__":
    main()