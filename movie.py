from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = '9c95f32d2ac2cd3f90e343920c70d576'

movie = Movie()

recommendations = movie.recommendations(movie_id=111)

for recommendation in recommendations:
    print(recommendation.title)
    print(recommendation.overview)