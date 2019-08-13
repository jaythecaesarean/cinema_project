import json
import re
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
#
from movies.serializers import MovieSerializer, MovieVariantSerializer, MovieFormatSerializer, \
                            MovieRatingSerializer, MovieCastSerializer
from movies.models import Movie, MovieVariant, MovieFormat, MovieRating, MovieCast
from .models import MovieSchedule, ScreenSeatType
from .serializers import MovieSchedule, MovieScheduleSerializer, ScreenSeatTypeSerializer
from theaters.serializers import CinemaSerializer


def parse_schedule_dict(data):
    price = float(data.get('price'))
    screening = data.get('screening', None)
    if screening:
        screening = datetime.strptime(screening, '%m/%d/%Y %I:%M:%S %p')
        print(screening)

    sched_data = {
        'external_id': data.get('id'),
        'cinema': {
            'name': data.get('cinema_name'),
            'code': data.get('cinema_code'),
            'theater': {
                'code': data.get('theater_code'),
            }
        },
        'price': price,
        'screening_datetime': screening,
        'seat_type': {
            'name': data.get('seat_type'),
        }
    }

    movies = MovieVariant.objects.filter(external_id=data.get('movie_id'))
    if movies:
        movie = movies.first()
        sched_data.update({'movie': movie.id})
    return sched_data


@api_view(['GET'])
def fetch_schedules(request):
    movie_schedule_json = settings.JSON_SCHEDULES
    with open(movie_schedule_json, 'r') as f:
        schedules_dict = json.load(f)
    response_data = schedules_dict.get('result', None)
    print(response_data)

    if isinstance(response_data, list):
        for item in response_data:
            sched_data = parse_schedule_dict(item)
            cinema_data = sched_data.pop('cinema')

            cinema_serializer = CinemaSerializer(data=cinema_data)
            if cinema_serializer.is_valid():
                new_cinema = cinema_serializer.save()
                sched_data.update({'cinema': new_cinema.id})
            else:
                print(cinema_serializer.errors)

            seat_type_serializer = ScreenSeatTypeSerializer(data=sched_data.pop('seat_type'))
            if seat_type_serializer.is_valid():
                new_seat_type = seat_type_serializer.save()
                sched_data.update({'seat_type': new_seat_type.id})
            else:
                print(seat_type_serializer.errors)

            schedule_serializer = MovieScheduleSerializer(data=sched_data)
            if schedule_serializer.is_valid():
                new_schedule = schedule_serializer.save()
            else:
                print(schedule_serializer.errors)

    return Response(status=status.HTTP_200_OK)
