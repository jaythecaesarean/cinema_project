import uuid
from django.db import models


class MovieSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    cinema = models.ForeignKey('theaters.Cinema', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    movie = models.ForeignKey('movies.MovieVariant', on_delete=models.CASCADE, null=True)
    screening_datetime = models.DateTimeField(null=True)
    seat_type = models.ForeignKey('ScreenSeatType', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.external_id


class ScreenSeatType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
