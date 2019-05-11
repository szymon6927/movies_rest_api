from django.conf import settings
import logging
import requests
from requests.exceptions import Timeout, TooManyRedirects, RequestException

LOGGER = logging.getLogger(__name__)


class OMDBMovie:
    ROOT_URL = f"http://www.omdbapi.com/?apikey={settings.OMDD_API_KEY}"

    def __init__(self, movie_title):
        self.movie_title = movie_title
        self.movie_info = self.get_movie_info()

    def get_movie_info(self):

        try:
            response = requests.get(f'{self.ROOT_URL}&t={self.movie_title}')

            if response.status_code == 200:
                LOGGER.info(f"Successfully fetched data for {self.movie_title} movie")
                return response.json()
            elif response.json()['Type'] != "movie":
                LOGGER.error(f"Looking for not a movie ({self.movie_title})")
                return None

            return None
        except Timeout:
            LOGGER.exception("Timeout form OMDB API")
            return None
        except TooManyRedirects:
            LOGGER.exception("To many redirects form OMDB API")
            return None
        except RequestException as e:
            LOGGER.exception(f"Request exception form OMDB API, full message {e}")
            return None

    @property
    def exist(self):
        """If 'Error' key exist in OMDB response that means the movie does not exist"""
        return 'Error' not in self.movie_info

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
    def ratings(self):
        return self.movie_info['Ratings']

    @property
    def metascore(self):
        try:
            return int(self.movie_info['Metascore'])
        except ValueError:
            return 0

    @property
    def imdb_rating(self):
        try:
            return float(self.movie_info['imdbRating'])
        except ValueError:
            return 0.0

    @property
    def imdb_votes(self):
        try:
            return float(self.movie_info['imdbVotes'].replace(",", "."))
        except ValueError:
            return 0.0
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
