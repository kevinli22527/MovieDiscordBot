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
    db = client["MovieBot"]
    users = db["Users"]

    megan_info = {"discord_name": "Megan", "discord_id": "656333371827421225", "display_name": "Megan", "watch_list": ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"], "turns_yielded": 0}

    kevin_info = {"discord_name": "Kevin", "discord_id": "279423302408339456", "display_name": "Kevin", "watch_list": ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"], "turns_yielded": 0}

    users.insert_many([megan_info, kevin_info])
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

#code needs to be tested when at home
def addToWatchList(discord_name, movie_name): #adds a movie to a user's watch list
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_name": discord_name})
    user_document["watch_list"].append(movie_name)

    # this new document will replace the old document
    users.replace_one({"discord_name": discord_name}, user_document)
    return


# client = getMongoClient()
# db = client["MovieBot"]
# users = db["WatchedMovies"]
# doc = {"watched_list": [{"nameOfMovie": "How to Train Your Dragon", "userRatings": [{"user": 279423302408339456, "rating": 9}]}]}
# users.insert_one(doc)

addWatchedMovie("How to Train Your Dragon 2")


#newvalues = {"$set": mydict}

#x = mycol.update_one(selection, newvalues)
#print(x.modified_count, "documents updated.")