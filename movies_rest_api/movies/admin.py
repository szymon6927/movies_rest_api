from django.contrib import admin
from movies.models import Movie, Comment, MovieRating


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'created',)
    ordering = ('-created',)


class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created',)
    ordering = ('-created',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text', 'created',)
    ordering = ('-created',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MovieRating, MovieRatingAdmin)
