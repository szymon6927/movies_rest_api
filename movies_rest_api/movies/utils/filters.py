from django_filters import rest_framework as filters

from ..models import Movie


class MovieFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = {
            'title': ['exact', 'icontains'],
        }
