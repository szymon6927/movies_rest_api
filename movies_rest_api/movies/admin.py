from django.contrib import admin
from movies.models import Movie, Comment, MovieRating


admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(MovieRating)