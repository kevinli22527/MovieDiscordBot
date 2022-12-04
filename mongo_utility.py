import pymongo


def getMongoClient():
    return pymongo.MongoClient("mongodb+srv://KevinLi:Kevinpower1@ourcluster.eemanbw.mongodb.net/?retryWrites=true&w=majority")


# this method drops all collections within a specified database
def drop_all_collections(target_database):
    client = getMongoClient()
    db = client[target_database]
    for collection in db.list_collection_names():
        db.drop_collection(collection)