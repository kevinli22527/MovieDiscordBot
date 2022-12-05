from tmdbv3api import TMDb
from tmdbv3api import Movie, Discover
from movie_utility import *

tmdb = TMDb()
tmdb.api_key = 'e373164d3c69c376e9af3610128d4b1a'

movie = Movie()
discover = Discover()

ID_TO_GENRE = {
    28: 'action',
    12: 'adventure',
    16: 'animation',
    35: 'comedy',
    80: 'crime',
    99: 'documentary',
    18: 'drama',
    10751: 'family',
    14: 'fantasy',
    36: 'history',
    27: 'horror',
    10402: 'music',
    9648: 'mystery',
    10749: 'romance',
    878: 'science fiction',
    10770: 'tv movie',
    53: 'thriller',
    10752: 'war',
    37: 'western'
}

GENRE_TO_ID = {
    'action': 28,
    'adventure': 12,
    'animation': 16,
    'comedy': 35,
    'crime': 80,
    'documentary': 99,
    'drama': 18,
    'family': 10751,
    'fantasy': 14,
    'history': 36,
    'horror': 27,
    'music': 10402,
    'mystery': 9648,
    'romance': 10749,
    'science fiction': 878,
    'tv movie': 10770,
    'thriller': 53,
    'war': 10752,
    'western': 37
}

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


# this method determines whether a movie actually exists in the TMDB database or not
def movieExists(movie_title):
    search_results = movie.search(movie_title)
    if (len(search_results) == 0):
        return False
    else:
        return True


# this method gets the english named genres of a movie specified by movie id, returns a list of strings
def getGenres(movie_name):
    search_results = movie.search(movie_name)
    if (len(search_results) == 0):
        return None
    else:
        first_result = search_results[0]
        genre_ids = first_result.genre_ids

        # map genre_ids to a list of string genres
        genres = []
        for genre_id in genre_ids:
            genres.append(ID_TO_GENRE[genre_id])
        return genres


# this method searches movies by genre names, refer to documentation for a list of valid genre names
def searchMoviesByGenre(genre_name):
    genre_id = GENRE_TO_ID[genre_name.lower()]
    search_results = discover.discover_movies({'with_genres': genre_id})
    result_list = []
    for result in search_results:
        result_list.append(result.title)
    return result_list


print(searchMoviesByGenre("action"))