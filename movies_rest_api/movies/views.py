from django.shortcuts import render
from django.db.models import Count

import datetime
import logging

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer

LOGGER = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'movies': reverse('all-movies', request=request, format=format),
        'comments': reverse('all-comments', request=request, format=format)
    })


class MovieListView(ListCreateAPIView):
    """
    Provides a get method handler.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CommentsListView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)

        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)

        return queryset


class TopMovieListView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        try:
            date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").date()

            movies_id = Comment.objects.filter(created__range=[date_from, date_to]).values_list('id', flat=True)

            top = Movie.objects.filter(id__in=movies_id).annotate(total_comments=Count('comment')).order_by(
                '-total_comments')

            return top
        except ValueError:
            LOGGER.exception('Date parsing error')

    def list(self, request, *args, **kwargs):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if not (date_from or date_to):
            return Response({"status": "Required field date_from and date_to not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(TopMovieListView, self).list(request, *args, **kwargs)
