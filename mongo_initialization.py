from mongo_utility import *
from mongo_users import *

# initializes all users in the database manually. Currently, this is for putting Megan and Kevin information into the Users collection
def initialize_users():
    client = getMongoClient()

    drop_all_collections("MovieBot")  # wipe all data in the database

    # reinitialize users collection
    db = client["MovieBot"]
    users = db["Users"]

    megan_info = {"discord_name": "Megan", "discord_id": "656333371827421225", "display_name": "Megan", "watch_list": [], "turns_yielded": 0}

    kevin_info = {"discord_name": "Kevin", "discord_id": "279423302408339456", "display_name": "Kevin", "watch_list": [], "turns_yielded": 0}

    users.insert_many([megan_info, kevin_info])

    # reinitialize watched movies collection
    watched_movies = db["WatchedMovies"]
    watched_movies_document = {"watched_list": []}
    watched_movies.insert_one(watched_movies_document) # this inserts the document into the collection

    # reinitialize logistics collection containing the index of the current turn user along with an array of user ids that are being selected from
    # first we get a list of all the user ids to add to the round robin selection pool
    user_info = get_all_users()
    user_ids = []
    for user in user_info:
        user_ids.append(user["discord_id"])

    # set up and add logistics document
    logistics = db["Logistics"]
    logistics_document = {"whose_turn": 0, "users": user_ids, "num_users": len(user_ids)}
    logistics.insert_one(logistics_document) # add the document to the collection
    return


def initialize_test_database():
    client = getMongoClient()

    drop_all_collections("MovieBot")  # wipe all data in the database

    # reinitialize users collection
    db = client["MovieBot"]
    users = db["Users"]

    megan_info = {"discord_name": "Megan", "discord_id": "656333371827421225", "display_name": "Megan", "watch_list": ["Ella Enchanted", "Jurassic Park", "Oceans 6"], "turns_yielded": 0}

    kevin_info = {"discord_name": "Kevin", "discord_id": "279423302408339456", "display_name": "Kevin", "watch_list": ["Mad Max", "Transformers"], "turns_yielded": 0}

    users.insert_many([megan_info, kevin_info])

    # reinitialize watched movies collection
    watched_movies = db["WatchedMovies"]
    watched_movies_document = {"watched_list": [{"nameOfMovie": "Despicable Me", "userRatings": []}]}
    watched_movies.insert_one(watched_movies_document) # this inserts the document into the collection

    # reinitialize logistics collection containing the index of the current turn user along with an array of user ids that are being selected from
    # first we get a list of all the user ids to add to the round robin selection pool
    user_info = get_all_users()
    user_ids = []
    for user in user_info:
        user_ids.append(user["discord_id"])

    # set up and add logistics document
    logistics = db["Logistics"]
    logistics_document = {"whose_turn": 0, "users": user_ids, "num_users": len(user_ids)}
    logistics.insert_one(logistics_document) # add the document to the collection
    return