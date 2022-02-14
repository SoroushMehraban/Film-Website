from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    """Movie model for showing a movie in a movie list"""
    name = models.CharField(max_length=100)
    poster = models.URLField(null=True, blank=True)
    director_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Comment from a user on a movie"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.user.username} on {self.movie}"
