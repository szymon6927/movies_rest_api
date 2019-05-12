from django.shortcuts import render
from django.db.models import Count
from django.db.models import F, Window
from django.db.models.functions import DenseRank
from django.conf import settings

import datetime
import logging

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django_filters import rest_framework as django_filters
from rest_framework import filters
from .utils.filters import MovieFilter

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer

LOGGER = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'movies': reverse('all-movies', request=request, format=format),
        'comments': reverse('all-comments', request=request, format=format),
        'top': reverse('top-movies', request=request, format=format)
    })


class MovieListView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing movies.

    post:
    Create a new movie. Set title and then all others information about movie will be fetched form OMDB API.
    Of course if you want to set all of the filed manually you can!
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('title',)
    filterset_class = MovieFilter
    ordering_fields = ('id', 'title', 'created')


class CommentsListView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing movie comments.

    Set 'movie_id' query params if you want list of comments for give movie
    Eg. /comments?movie_id=1

    post:
    Create a new comment for given movie.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)

        if movie_id:
            queryset = queryset.filter(movie__id=movie_id)

        return queryset


class TopMovieListView(ListAPIView):
    """
    get:
    Return a rank list of top movies in given date range based on comments count.

    Required query_params:
    - date_from (d-m-Y)
    - date_to (d-m-Y)

    eg. /top?date_from=10-05-2019&date_to=12-05-2019
    """
    serializer_class = MovieSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        try:
            date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").date()

            if settings.USING_SQLLITE:
                top_movies = Movie.objects.filter(
                    comment__created__range=[date_from, date_to]
                ).annotate(
                    total_comments=Count('comment')
                ).order_by('-total_comments')

                return top_movies
            else:
                dense_rank_by_total_comments = Window(
                    expression=DenseRank(),
                    order_by=F("total_comments").desc()
                )

                top_movies = Movie.objects.filter(
                    comment__created__range=[date_from, date_to]
                ).annotate(
                    total_comments=Count('comment')
                ).annotate(
                    rank=dense_rank_by_total_comments
                ).order_by('-total_comments')

                return top_movies
        except ValueError:
            LOGGER.exception('Date parsing error')

    def build_response_sqlite(self):
        json_response = []
        queryset = self.get_queryset()

        rank = 0
        previous_comment_number = None

        for movie in queryset:
            if previous_comment_number != movie.total_comments:
                rank += 1

            previous_comment_number = movie.total_comments

            json_response.append({"movie_id": movie.id,
                                  "total_comments": movie.total_comments,
                                  "rank": rank})

        return json_response

    def build_response(self):
        json_response = []
        queryset = self.get_queryset()

        for movie in queryset:
            json_response.append({"movie_id": movie.id,
                                  "total_comments": movie.total_comments,
                                  "rank": movie.rank})

        return json_response

    def list(self, request, *args, **kwargs):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if not (date_from or date_to):
            return Response({"status": "Required field date_from and date_to not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        json_response = self.build_response_sqlite() if settings.USING_SQLLITE else self.build_response()

        return Response(json_response, status=status.HTTP_200_OK)
