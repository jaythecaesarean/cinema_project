from rest_framework import serializers

from .models import Theater, Cinema



class TheaterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theater
        fields = ['code']



class CinemaSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer()
    class Meta:
        model = Cinema
        fields = ['code', 'name', 'theater',]

    def create(self, validated_data):
        print("<<<<<<<<<<", validated_data)
        theater = validated_data.pop('theater')
        theater, created = Theater.objects.update_or_create(code=theater.get('code'))
        validated_data.update({'theater': theater})
        cinema, created = Cinema.objects.update_or_create(code=validated_data.get('code'),
                                                          name=validated_data.get('name'),
                                                                   defaults=validated_data)
        return cinema