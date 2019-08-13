import json
import re
from datetime import datetime, date

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from .serializers import MovieSerializer, MovieVariantSerializer, MovieFormatSerializer, \
                            MovieRatingSerializer, MovieCastSerializer
from .models import Movie, MovieVariant, MovieFormat, MovieRating, MovieCast
from schedules.models import MovieSchedule


def parse_movie_data(movie_data):
    movie_title = movie_data.get('movie_title', None)
    format = None
    if re.search("^\((.*?)\) ", movie_title):
        format = {
            'name': re.findall("^\((.*?)\) ", movie_title)[0]
        }
        movie_title = re.findall("^\(.*?\) (.*)$", movie_title)[0]
    release_date = movie_data.get('release_date', None)
    if release_date:
        release_date = datetime.strptime(release_date, '%Y/%m/%d').date()

    formatted_movie_data = {
        "title": movie_title,
        "casts": [{'name': cast} for cast in movie_data.get('cast', [])],
        "synopsis": movie_data.get('synopsis', None),
        "rating": {'rating': movie_data.get('rating', None)},
        "image_url": movie_data.get('image_url', None),
        "release_date": release_date
    }

    variant_data = {
        "external_id": movie_data.get('id'),
        "format": None
    }

    if format:
        format_data = {
            "format": format
        }
        variant_data.update(format_data)

    return variant_data, formatted_movie_data


def get_movie_by_variant_id(external_id):
    movie = MovieVariant.objects.filter(external_id=external_id)
    if movie:
        return movie.values_list('id', flat=True).first()
    return None


def fetch_movies(request, category=None):
    if category == 'coming_soon':
        movies_json = settings.JSON_COMING_SOON
    else:
        movies_json = settings.JSON_NOW_SHOWING
        
    with open(movies_json, 'r') as f:
        movie_dict = json.load(f)
    response_data = movie_dict.get('results', None)

    if isinstance(response_data, list):
        for item in response_data:
            variant_data, movie_data = parse_movie_data(item)
            movie_serializer = MovieSerializer(data=movie_data)
            if movie_serializer.is_valid():
                new_movie = movie_serializer.save()
            else:
                print(movie_serializer.errors)

            variant_data.update({'movie': new_movie.id})
            movie_variant_serializer = MovieVariantSerializer(data=variant_data)
            if movie_variant_serializer.is_valid():
                movie_variant_serializer.save()
            else:
                print(movie_variant_serializer.errors)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def fetch_coming_soon(request):
    return fetch_movies(request, 'coming_soon')


@api_view(['GET'])
def fetch_now_showing(request):
    return fetch_movies(request, 'now_showing')


@api_view(['GET'])
def retrieve_movies(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        movie_data = {
            'id': str(movie.id),
            'movie': {
                'advisory_rating': movie.rating.rating if movie.rating else '',
                'canonical_title': movie.title,
                'cast': [cast.name for cast in movie.casts.all()],
                'poster_portrait': movie.image_url or '',
                'release_date': movie.release_date or '',
                'synopsis': movie.synopsis,
                'variants': [variant.format.name for variant in MovieVariant.objects.filter(movie=movie) if variant.format]
            }
        }
        movie_list.append(movie_data)
    print(movie_list)

    return Response(movie_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def retrieve_movie_schedules(request, movie_id):
    movies = Movie.objects.all().filter(id=movie_id)
    if movies:
        variants = MovieVariant.objects.all().filter(movie__in=movies)
        schedules = MovieSchedule.objects.all().filter(movie__in=variants)
        if 'show_date' in request.query_params:
            query_date = request.query_params['show_date']
            show_date = datetime.strptime(query_date, '%m/%d/%Y').date()
            schedules = schedules.filter(screening_datetime__date=show_date)

        schedule_list = []
        for schedule in schedules:
            screen_datetime = schedule.screening_datetime
            screen_date = screen_datetime.strftime("%d %b %Y")
            screen_time = screen_datetime.strftime("%H:%M")
            sched_data = {
                'id': str(schedule.id),
                'schedule': {
                    'cinema': schedule.cinema.code,
                    'movie': schedule.movie.movie.id,
                    'price': schedule.price,
                    'seating_type': schedule.seat_type.name,
                    'show_date': screen_date,
                    'start_times': [screen_time],
                    'theater': schedule.cinema.theater.name,
                    'variant': schedule.movie.format.name if schedule.movie.format else None
                }
            }
            schedule_list.append(sched_data)
        if schedule_list:
            return Response(schedule_list, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)