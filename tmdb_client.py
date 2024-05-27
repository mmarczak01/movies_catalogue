import requests
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMzMxODk1ODg4Mjc5Y2E1MTYzZjhlZTMxYTU4NTA3NyIsInN1YiI6IjY2MzdhMGZkNDcwZWFkMDEyODEyZmEzMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1awmg1b1O97PT9q77xyHIbKsLPP4yQcuxjIYi0Dlgl0"
lists = ["popular", "top_rated", "upcoming", "now_playing"]


def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   if "/credits" in endpoint:
        return response.json()["cast"]
   else:
        return response.json()

def get_popular_movies():
    return call_tmdb_api(f"movie/{lists[0]}")

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many, list_type):
    if list_type == "popular" or list_type not in lists:
        data = get_popular_movies()
    else:
        data = get_movies_list(list_type)
    return data["results"][:how_many]

def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")

def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")

def get_casts(how_many, movie_id):
    data = get_single_movie_cast(movie_id)
    return data[:how_many]

def get_movies_list(list_type):
    return call_tmdb_api(f"movie/{list_type}")