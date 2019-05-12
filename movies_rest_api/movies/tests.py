from django.urls import reverse

import json
import logging
import datetime

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from .utils.omdb import OMDBMovie


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.movie_1 = self.create_movie("Movie 1")
        self.movie_2 = self.create_movie("Movie 2")

        self.comment_1 = self.create_comment(movie=self.movie_1.id, comment_text="Test comment 1")
        self.comment_2 = self.create_comment(movie=self.movie_2.id, comment_text="Test comment 2")

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @staticmethod
    def create_movie(title=""):
        if title != "":
            return Movie.objects.create(title=title)

    @staticmethod
    def create_comment(movie, comment_text):
        if movie and comment_text:
            return Comment.objects.create(movie_id=movie, text=comment_text)


class MoviesTests(BaseViewTest):

    def test_get_all_movies(self):
        """
        This test ensures that all movies added in the setUp method
        exist when we make a GET request to the movies/ endpoint
        """

        response = self.client.get(reverse("all-movies"))

        expected = Movie.objects.all()
        serialized = MovieSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_omdbi_api_object(self):
        movie = OMDBMovie("Batman")

        self.assertTrue(isinstance(movie, OMDBMovie))
        self.assertEqual(movie.exist, True)

    def test_ombbi_api_object_when_movie_not_exist(self):
        movie = OMDBMovie("Not existing movie")

        self.assertTrue(isinstance(movie, OMDBMovie))
        self.assertEqual(movie.exist, False)

    def test_post_movie(self):
        payload = {
            'title': "Titanic"
        }

        response = self.client.post(reverse("all-movies"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_top_movies(self):
        movie_1 = Movie.objects.create(title="Batman")
        movie_2 = Movie.objects.create(title="Spiderman")
        movie_3 = Movie.objects.create(title="Dirty Dancing")

        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 10))
        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 11))
        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 12))

        Comment.objects.create(movie=movie_2, created=datetime.datetime(2019, 5, 10))
        Comment.objects.create(movie=movie_2, created=datetime.datetime(2019, 5, 11))

        Comment.objects.create(movie=movie_3, created=datetime.datetime(2019, 5, 10))

        payload = {
            'date_from': "10-05-2019",
            'date_to': "12-05-2019"
        }

        response = self.client.get(reverse("top-movies"), payload)

        expected_response = [
            {
                "movie_id": movie_1.id,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": movie_2.id,
                "total_comments": 2,
                "rank": 2
            },
            {
                "movie_id": movie_3.id,
                "total_comments": 1,
                "rank": 3
            }
        ]

        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_movies_the_same_rank(self):
        movie_1 = Movie.objects.create(title="Batman")
        movie_2 = Movie.objects.create(title="Spiderman")
        movie_3 = Movie.objects.create(title="Dirty Dancing")

        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 10))
        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 11))
        Comment.objects.create(movie=movie_1, created=datetime.datetime(2019, 5, 12))

        Comment.objects.create(movie=movie_2, created=datetime.datetime(2019, 5, 10))
        Comment.objects.create(movie=movie_2, created=datetime.datetime(2019, 5, 11))
        Comment.objects.create(movie=movie_2, created=datetime.datetime(2019, 5, 12))

        Comment.objects.create(movie=movie_3, created=datetime.datetime(2019, 5, 10))

        payload = {
            'date_from': "10-05-2019",
            'date_to': "12-05-2019"
        }

        response = self.client.get(reverse("top-movies"), payload)

        expected_response = [
            {
                "movie_id": movie_1.id,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": movie_2.id,
                "total_comments": 3,
                "rank": 1
            },
            {
                "movie_id": movie_3.id,
                "total_comments": 1,
                "rank": 2
            }
        ]

        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_movies_when_data_range_not_given(self):
        response = self.client.get(reverse("top-movies"))

        expected_response = {
            'status': "Required field date_from and date_to not found."
        }

        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentsTest(BaseViewTest):

    def test_get_all_comments(self):
        response = self.client.get(reverse("all-comments"))

        expected = Comment.objects.all()
        serialized = CommentSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_commment_for_given_movie(self):
        response = self.client.get(reverse("all-comments"), {'movie_id': self.movie_1.id})

        expected = Comment.objects.get(movie=self.movie_1)
        serialized = CommentSerializer(expected)

        self.assertEqual(json.loads(response.content)[0], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_commment_for_given_movie_which_not_exist(self):
        not_existing_movie_id = 100

        response = self.client.get(reverse("all-comments"), {'movie_id': not_existing_movie_id})

        expected = Comment.objects.filter(movie__id=not_existing_movie_id)

        self.assertEqual(len(response.data), len(expected))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment(self):
        payload = {
            'movie': self.movie_1.id,
            'text': "Test comment for movie 1"
        }

        response = self.client.post(reverse("all-comments"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
