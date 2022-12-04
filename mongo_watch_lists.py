from mongo_utility import *


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
    return movie_name.lower() in [movie.lower() for movie in watch_list]


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


# this method moves a movie from a user's watch list to the collective watched list
def moveFromUserWatchListToWatched(discord_id, movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]
    watched_movies = db["WatchedMovies"]

    # get the document for the user as a Python dictionary
    user_document = users.find_one({"discord_id": discord_id})
    watch_list = user_document["watch_list"]
    watch_list.remove(movie_name)

    # this new document will replace the old document
    users.replace_one({"discord_id": discord_id}, user_document)

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    movie_info = {"nameOfMovie": movie_name, "userRatings": []}
    watched_movies_document["watched_list"].append(movie_info)

    # this new document will replace the old document
    watched_movies.replace_one({}, watched_movies_document)
    return


# this method returns the collective watched list, as a list of dictionaries
def getWatchedMovies():
    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    watched_list = watched_movies_document["watched_list"]
    return watched_list


# this method returns whether the movie has been watched before (in the collective watched list) given the movie name
def haveWatchedBefore(movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    watched_list = watched_movies_document["watched_list"]
    for movie in watched_list:
        if movie["nameOfMovie"].lower() == movie_name.lower():
            return True
    return False