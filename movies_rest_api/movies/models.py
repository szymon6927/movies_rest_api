from django.db import models
from django.utils import timezone
import logging

from .utils.omdb import OMDBMovie

LOGGER = logging.getLogger(__name__)


class Movie(models.Model):
    title = models.CharField(max_length=150, unique=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    rated = models.CharField(max_length=10, null=True, blank=True)
    released = models.CharField(max_length=15, null=True, blank=True)
    runtime = models.CharField(max_length=10, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=150, null=True, blank=True)
    writer = models.TextField(null=True, blank=True)
    actors = models.TextField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    awards = models.CharField(max_length=100, null=True, blank=True)
    poster = models.CharField(max_length=250, null=True, blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    imdb_votes = models.FloatField(null=True, blank=True)
    imdb_id = models.CharField(max_length=15, null=True, blank=True)
    dvd = models.CharField(max_length=20, null=True, blank=True)
    box_office = models.CharField(max_length=10, null=True, blank=True)
    production = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        movie = OMDBMovie(self.title)

        if movie.exist:
            LOGGER.info(f"Succesfully fetched data for movie {self.title}")
            self.year = movie.year
            self.rated = movie.rated
            self.released = movie.released
            self.runtime = movie.runtime
            self.genre = movie.genre
            self.director = movie.director
            self.writer = movie.writer
            self.actors = movie.actors
            self.plot = movie.plot
            self.language = movie.language
            self.country = movie.country
            self.awards = movie.awards
            self.poster = movie.poster
            self.metascore = movie.metascore
            self.imdb_rating = movie.imdb_rating
            self.imdb_votes = movie.imdb_votes
            self.imdb_id = movie.imdb_id
            self.dvd = movie.dvd
            self.box_office = movie.boxoffice
            self.production = movie.production
            self.website = movie.website

        LOGGER.info(f"Succesfully store movie {self.title} in DB")

        super(Movie, self).save(*args, **kwargs)

        self.save_movie_ratings(movie=movie)

    def save_movie_ratings(self, movie):
        if movie.exist:
            for rating in movie.ratings:
                MovieRating.objects.create(movie_id=self.id, source=rating.get('Source', None),
                                           value=rating.get('Value', None))
                LOGGER.info(f"Succesfully store movie rating in DB")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "movies"


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Comment for {self.movie.title}'

    class Meta:
        verbose_name_plural = "comments"


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    source = models.CharField(max_length=150)
    value = models.CharField(max_length=10)
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Rating (OMDb API) for {self.movie.title} movie'

    class Meta:
        verbose_name_plural = "ratings"
