from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from .views import MovieListView, CommentsListView, TopMovieListView, api_root

schema_view = get_swagger_view(title='Movies REST API')

urlpatterns = [
    path('movies/', MovieListView.as_view(), name="all-movies"),
    path('comments/', CommentsListView.as_view(), name="all-comments"),
    path('top/', TopMovieListView.as_view(), name="top-movies"),
    path('docs/', schema_view),
    path('', api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)
