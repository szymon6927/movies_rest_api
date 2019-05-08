from django.contrib import admin
from movies.models import Movie, Comment


admin.site.register(Movie)
admin.site.register(Comment)
