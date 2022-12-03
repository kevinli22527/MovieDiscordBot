import pymongo

def getMongoClient():
    return pymongo.MongoClient("mongodb+srv://KevinLi:Kevinpower1@ourcluster.eemanbw.mongodb.net/?retryWrites=true&w=majority")


# this method drops all collections within a specified database
def drop_all_collections(target_database):
    client = getMongoClient()
    db = client[target_database]
    for collection in db.list_collection_names():
        db.drop_collection(collection)


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
    logistics_document = {"whose_turn": 0, "users": user_ids}
    logistics.insert_one(logistics_document) # add the document to the collection
    return


# takes the discord name, discord id, and display name of a user and adds them to the database. Watch list will be empty and turns yielded will be 0 initially
def add_user(discord_name, discord_id, display_name):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]
    user_info = {"discord_name": discord_name, "discord_id": discord_id, "display_name": display_name, "watch_list": [], "turns_yielded": 0}
    return


# returns information for all users in the database as a list of dictionaries (hashmaps)
def get_all_users():
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]
    user_info = list(users.find({}))  # this queries the database for all users
    # print type of user info
    return user_info


# adds a movie to the collective watch list. Ratings will be empty initially
def addWatchedMovie(movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    movie_info = {"nameOfMovie": movie_name, "userRatings": []}
    watched_movies_document["watched_list"].append(movie_info)

    # this new document will replace the old document
    watched_movies.replace_one({}, watched_movies_document)
    return


# adds the movie name to a user's watch list; user identified by the user id
def addToWatchList(discord_id, movie_name): 
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_id": discord_id})
    user_document["watch_list"].append(movie_name)

    # this new document will replace the old document
    users.replace_one({"discord_id": discord_id}, user_document)
    return


# this method returns whether a movie name is inside a user's watch list; user is identified by the user id
def isInUserWatchList(discord_id, movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_id": discord_id})
    watch_list = user_document["watch_list"]
    return movie_name in watch_list

# this method returns all of the movies inside a user's watch list
def getUserWatchList(discord_id):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_id": discord_id})
    watch_list = user_document["watch_list"]
    return watch_list

# this method removes a movie from inside a user's watch list
def removeFromUserWatchList(discord_id, movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_id": discord_id})
    watch_list = user_document["watch_list"]
    watch_list.remove(movie_name)

    # this new document will replace the old document
    users.replace_one({"discord_id": discord_id}, user_document)
    return