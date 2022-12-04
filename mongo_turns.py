from mongo_utility import *


# this method determines which user is next in the round robin selection, returns the user document as a Python dictionary
def getWhoseTurn():
    client = getMongoClient()
    db = client["MovieBot"]
    logistics = db["Logistics"]
    users = db["Users"]

    # get the document for the logistics as a Python dictionary
    logistics_document = logistics.find_one({})
    whose_turn = logistics_document["whose_turn"]
    user_ids = logistics_document["users"]
    # get discord id of the user whose turn it is
    user_id = user_ids[whose_turn]
    # get the user discord name
    user_document = users.find_one({"discord_id": user_id})
    return user_document

# this method updates the round robin selection
def updateWhoseTurn():
    client = getMongoClient()
    db = client["MovieBot"]
    logistics = db["Logistics"]

    # get the document for the logistics as a Python dictionary
    logistics_document = logistics.find_one({})
    whose_turn = logistics_document["whose_turn"]
    num_users = logistics_document["num_users"]

    # update the round robin selection
    logistics_document["whose_turn"] = (whose_turn + 1) % num_users
    
    # this new document will replace the old document
    logistics.replace_one({}, logistics_document)
    return


# this method allows a user to yield a turn selecting the movie. discord id identifies the user
def yieldYourTurn(discord_id):
    client = getMongoClient()
    db = client["MovieBot"]
    logistics = db["Logistics"]
    users = db["Users"]

    # get the document for the logistics as a Python dictionary
    logistics_document = logistics.find_one({})
    whose_turn = logistics_document["whose_turn"]
    user_ids = logistics_document["users"]
    # get discord id of the user whose turn it is
    user_id = user_ids[whose_turn]
    # get the user discord name
    user_document = users.find_one({"discord_id": user_id})
    # update the turns yielded
    user_document["turns_yielded"] += 1
    # update the user document
    users.replace_one({"discord_id": user_id}, user_document)
    # update the round robin selection
    updateWhoseTurn()