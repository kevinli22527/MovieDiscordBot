from mongo_utility import *


# this method returns the rating of a user for a movie as a float, assume inputs are valid, otherwise return none
def getUserRating(discord_id, movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    watched_list = watched_movies_document["watched_list"]
    for movie_info in watched_list: # lock the movie name
        if movie_info["nameOfMovie"] == movie_name:
            user_ratings = movie_info["userRatings"]
            for user_rating in user_ratings:  # lock the user rating if it exists
                if user_rating["discord_id"] == discord_id:
                    return user_rating["rating"]
    return None


# this method rates a movie for a user, assume inputs are valid
# rating should be a string or float
def addUserRating(discord_id, movie_name, rating):

    rating = float(rating)

    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    watched_list = watched_movies_document["watched_list"]
    for movie_info in watched_list:
        if movie_info["nameOfMovie"] == movie_name:
            for rating_info in movie_info["userRatings"]:
                if rating_info["discord_id"] == discord_id:
                    rating_info["rating"] = rating
                    watched_movies.replace_one({}, watched_movies_document)
                    return
            movie_info["userRatings"].append({"discord_id": discord_id, "rating": rating})  # has not returned - append a new rating since user has not rated before
            break

    # this new document will replace the old document
    watched_movies.replace_one({}, watched_movies_document)
    return
    
# determines if a rating is valid. rating is passed in as a string or float
def isValidRating(rating):
    try:
        rating = float(rating)
        if rating < 0 or rating > 10:
            return False
        return True
    except ValueError:
        return False


# gets the ratings for a movie in the watched list as a list
def getMovieRatings(movie_name):
    client = getMongoClient()
    db = client["MovieBot"]
    watched_movies = db["WatchedMovies"]

    # get the document for the watched movies as a Python dictionary
    watched_movies_document = watched_movies.find_one({})
    watched_list = watched_movies_document["watched_list"]
    for movie_info in watched_list:
        if movie_info["nameOfMovie"].lower() == movie_name.lower():
            return movie_info["userRatings"]
    return None