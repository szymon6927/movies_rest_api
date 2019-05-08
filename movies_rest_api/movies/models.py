from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "movies"


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Comment for {self.movie.name}'

    class Meta:
        verbose_name_plural = "comments"
