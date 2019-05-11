from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_movie(title=""):
        if title != "":
            return Movie.objects.create(title=title)

    @staticmethod
    def create_comment(movie, comment_text):
        if movie and comment_text:
            return Comment.objects.create(movie_id=movie, text=comment_text)

    def setUp(self):
        movie_1 = self.create_movie("Movie 1")
        movie_2 = self.create_movie("Movie 2")
        self.create_comment(movie=movie_1.id, comment_text="Test comment 1")
        self.create_comment(movie=movie_2.id, comment_text="Test comment 2")


class GetAllMoviesTest(BaseViewTest):

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


class PostMoviesTest(BaseViewTest):
    def test_post_movie(self):
        movie_title = "Titanic"


class GetCommentsTest(BaseViewTest):
    def test_get_all_comments(self):
        response = self.client.get(reverse("all-comments"))

        expected = Comment.objects.all()
        serialized = CommentSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_commment_for_given_movie(self):
        pass
