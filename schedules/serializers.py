from rest_framework import serializers

from .models import MovieSchedule, ScreenSeatType
from theaters.models import Theater, Cinema
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
    movie = serializers.PrimaryKeyRelatedField(queryset=MovieVariant.objects.all())
    class Meta:
        model = MovieSchedule
        fields = ['external_id', 'cinema', 'price', 'movie',
                  'screening_datetime', 'seat_type']

    def create(self, validated_data):
        cinema = validated_data.get('cinema')
        movie = validated_data.get('movie')
        seat_type = validated_data.get('seat_type')
        schedule, created = MovieSchedule.objects.update_or_create(external_id=validated_data.get('external_id'),
                                                                   defaults=validated_data)
        return schedule

