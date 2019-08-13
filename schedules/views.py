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
    movie_title = data.get('movie_title')
    if re.search("^\((.*?)\) ", movie_title):
        format = {
            'name': re.findall("^\((.*?)\) ", movie_title)[0]
        }
        movie_title = re.findall("^\(.*?\) (.*)$", movie_title)[0]
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
        # 'movie': movies.first(),
        #     {
        #     'external_id': data.get('movie_id'),
        #     # 'title': movie_title,
        #     'format': {'name':data.get('variant')},
        # },
        'screening_datetime': screening,
        'seat_type': {
            'name': data.get('seat_type'),
        }
    }

    movies = MovieVariant.objects.filter(external_id=data.get('movie_id'))
    if movies:
        movie = movies.first()
        print(">>>>>>>>>", movie, movie.id)
        sched_data.update({'movie': movie.id})
    return sched_data


@api_view(['GET'])
def fetch_schedules(request):
    movie_schedule_json = settings.JSON_SCHEDULES
    print(movie_schedule_json)
    with open(movie_schedule_json, 'r') as f:
        schedules_dict = json.load(f)
    response_data = schedules_dict.get('result', None)
    print(response_data)

    if isinstance(response_data, list):
        for item in response_data:
            sched_data = parse_schedule_dict(item)
            cinema_data = sched_data.pop('cinema')
            print(cinema_data)
            cinema_serializer = CinemaSerializer(data=cinema_data)
            if cinema_serializer.is_valid():
                new_cinema = cinema_serializer.save()
                sched_data.update({'cinema': new_cinema.id})
                print("+================+", sched_data)
            else:
                print(cinema_serializer.errors)

            seat_type_serializer = ScreenSeatTypeSerializer(data=sched_data.pop('seat_type'))
            if seat_type_serializer.is_valid():
                new_seat_type = seat_type_serializer.save()
                sched_data.update({'seat_type': new_seat_type.id})
            else:
                print(seat_type_serializer.errors)
            # movie_variant_data = sched_data.pop('movie')
            # movie_variant_serializer = MovieVariantSerializer(data=movie_variant_data)
            # if movie_variant_serializer.is_valid():
            #     new_movie_variant = movie_variant_serializer.save()
            #     sched_data.update({'movie': new_movie_variant.id})
            # else:
            #     print(movie_variant_serializer.errors)
            print("sched_data =====>", sched_data)
            schedule_serializer = MovieScheduleSerializer(data=sched_data)
            if schedule_serializer.is_valid():
                new_schedule = schedule_serializer.save()
            else:
                print(schedule_serializer.errors)

    return Response(status=status.HTTP_200_OK)
