from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MovieListView, CommentsListView, TopMovieListView, api_root

urlpatterns = [
    path('movies/', MovieListView.as_view(), name="all-movies"),
    path('comments/', CommentsListView.as_view(), name="all-comments"),
    path('top/', TopMovieListView.as_view(), name="top-commented-movie"),
    path('', api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)
