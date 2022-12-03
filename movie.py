from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'e373164d3c69c376e9af3610128d4b1a'

movie = Movie()

# gets recommendations based on previously watched movie
def get_recommendations(movie_title):
    #get id of movie
    search_results = movie.search(movie_title)
    if (len(search_results) == 0):
        # raise exception
        raise Exception("Movie not found")
    else:
        movie_id = search_results[0].id
    #get recommendations
    recommendations = movie.recommendations(movie_id)
    for recommendation in recommendations:
        print(recommendation.title)
        print(recommendation.id)
        print(recommendation.overview)
        print(recommendation.genres)
        print()
try:
    get_recommendations('The Lion King')
except Exception as e:
    print("exception occurred")


# this method determines whether a movie actually exists in the TMDB database or not
def movieExists(movie_title):
    search_results = movie.search(movie_title)
    if (len(search_results) == 0):
        return False
    else:
        return True