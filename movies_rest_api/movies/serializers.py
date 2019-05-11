from rest_framework import serializers

from movies.models import Movie, Comment, MovieRating


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ('source', 'value')


class MovieSerializer(serializers.ModelSerializer):
    ratings = MovieRatingSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'rated', 'released', 'runtime', 'genre', 'director', 'writer', 'actors',
                  'plot', 'language', 'country', 'awards', 'poster', 'ratings', 'metascore', 'imdb_rating',
                  'imdb_votes', 'imdb_id', 'dvd', 'box_office', 'production', 'website', 'created', 'updated',)
        extra_kwargs = {'title': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'text')
