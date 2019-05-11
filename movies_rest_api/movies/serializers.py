from rest_framework import serializers

from movies.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'created', 'updated', 'year')
        extra_kwargs = {'title': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'movie', 'text')
