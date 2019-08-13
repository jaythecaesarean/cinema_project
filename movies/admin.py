from django.contrib import admin

from .models import Movie, MovieCast, MovieRating, MovieVariant, MovieFormat

admin.site.register(Movie)
admin.site.register(MovieCast)
admin.site.register(MovieRating)
admin.site.register(MovieVariant)
admin.site.register(MovieFormat)
