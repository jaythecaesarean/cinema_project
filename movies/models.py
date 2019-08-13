import uuid
from django.db import models


class MovieRating(models.Model):
    rating = models.CharField(max_length=200)

    def __str__(self):
        return self.rating


class MovieVariant(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    format = models.ForeignKey('MovieFormat', blank=True, on_delete=models.DO_NOTHING, null=True)

    def get_name(self):
        if self.format:
            return "({}) {}".format(self.format, self.movie.title)
        return self.movie.title

    name = property(get_name)

    def __str__(self):
        return self.name


class MovieCast(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class MovieFormat(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    rating = models.ForeignKey('MovieRating', on_delete=models.CASCADE, null=True)
    synopsis = models.TextField()
    image_url = models.URLField()
    release_date = models.DateField(null=True)
    casts = models.ManyToManyField('MovieCast')

    def __str__(self):
        return self.title

    def get_movie_by_title(self, title):
        movie_instance = self.objects.filter(title=title)
        return movie_instance.first() if movie_instance else None
