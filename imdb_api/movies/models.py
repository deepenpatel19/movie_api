from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    released_year = models.CharField(max_length=4, blank=True, null=True)
    rating = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Genres(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='genres_movie')

    def __str__(self):
        return str(self.id)

