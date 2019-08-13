from rest_framework import serializers

from .models import MovieSchedule, ScreenSeatType
from theaters.models import Theater, Cinema
from theaters.serializers import CinemaSerializer
from movies.serializers import MovieVariantSerializer
from movies.models import MovieVariant


class ScreenSeatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenSeatType
        fields = ['name']

    def create(self, validated_data):
        seat_type, created = ScreenSeatType.objects.update_or_create(name=validated_data['name'])
        return seat_type

class MovieScheduleSerializer(serializers.ModelSerializer):
    cinema = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all())
    seat_type = serializers.PrimaryKeyRelatedField(queryset=ScreenSeatType.objects.all())
    # seat_type = ScreenSeatTypeSerializer()
    # movie = MovieVariantSerializer()
    movie = serializers.PrimaryKeyRelatedField(queryset=MovieVariant.objects.all())
    class Meta:
        model = MovieSchedule
        fields = ['external_id', 'cinema', 'price', 'movie',
                  'screening_datetime', 'seat_type']

    def create(self, validated_data):
        print(validated_data,">>>>>>>>>>>>>>>>>>")
        cinema = validated_data.get('cinema')
        movie = validated_data.get('movie')
        seat_type = validated_data.get('seat_type')

        # if cinema:
        #     cinema, created = Cinema.object.update_or_create(code=cinema['code'], name=cinema['name'])
        # seat_type, created = ScreenSeatType.objects.update_or_create(name=seat_type['name'])
        # validated_data.update({'seat_type': seat_type.id})
        # print(validated_data)
        schedule, created = MovieSchedule.objects.update_or_create(external_id=validated_data.get('external_id'),
                                                                   defaults=validated_data)
        return schedule

