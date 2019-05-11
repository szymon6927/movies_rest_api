from django.conf import settings
import requests


class OMDBMovie:
    ROOT_URL = f"http://www.omdbapi.com/?apikey={settings.OMDD_API_KEY}"

    def __init__(self, movie_title):
        self.movie_title = movie_title
        self.movie_info = self.get_movie_info()

    def get_movie_info(self):
        response = requests.get(f'{self.ROOT_URL}&t={self.movie_title}')

        if response.status_code == 200:
            return response.json()
        elif response.json()['Type'] != "movie":
            print("You are searching not a movie")
            return {}
        else:
            print("Somthing wrong! Try again")
            return {}

    @property
    def year(self):
        return self.movie_info['Year']

    @property
    def rated(self):
        return self.movie_info['Rated']

    @property
    def released(self):
        return self.movie_info['Released']

    @property
    def runtime(self):
        return self.movie_info['Runtime']

    @property
    def genre(self):
        return self.movie_info['Genre']

    @property
    def director(self):
        return self.movie_info['Director']

    @property
    def writer(self):
        return self.movie_info['Writer']

    @property
    def actors(self):
        return self.movie_info['Actors']

    @property
    def plot(self):
        return self.movie_info['Plot']

    @property
    def language(self):
        return self.movie_info['Language']

    @property
    def country(self):
        return self.movie_info['Country']

    @property
    def awards(self):
        return self.movie_info['Awards']

    @property
    def poster(self):
        return self.movie_info['Poster']

    @property
    def metascore(self):
        return int(self.movie_info['Metascore'])

    @property
    def imdb_rating(self):
        return float(self.movie_info['imdbRating'])

    @property
    def imdb_votes(self):
        return float(self.movie_info['imdbVotes'].replace(",", "."))

    @property
    def imdb_id(self):
        return self.movie_info['imdbID']

    @property
    def dvd(self):
        return self.movie_info['DVD']

    @property
    def boxoffice(self):
        return self.movie_info['BoxOffice']

    @property
    def production(self):
        return self.movie_info['Production']

    @property
    def website(self):
        return self.movie_info['Website']
