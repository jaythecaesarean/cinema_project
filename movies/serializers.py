from rest_framework import serializers

from .models import Movie, MovieCast, MovieVariant, MovieRating, MovieFormat


class MovieFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFormat
        fields = ['id', 'name']


class MovieCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCast
        fields = ['id', 'name']


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ['rating']

    def create(self, validated_data):
        rating, created = MovieRating.objects.update_or_create(rating=validated_data.get('rating'))
        return rating


class MovieSerializer(serializers.ModelSerializer):
    rating = MovieRatingSerializer()
    casts = MovieCastSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'synopsis', 'image_url', 'release_date', 'rating', 'casts']
        extra_kwargs = {
            'title': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        casts_list = validated_data.pop('casts')
        rating_item = validated_data.pop('rating')
        casts = []
        rating, created = MovieRating.objects.update_or_create(rating=rating_item['rating'])
        validated_data.update({'rating': rating})
        movie, created = Movie.objects.update_or_create(title=validated_data.get('title'),
                                                        defaults=validated_data)
        for cast in casts_list:
            cast_instance, created = MovieCast.objects.update_or_create(name=cast['name'])
            movie.casts.add(cast_instance)
        return movie


class MovieVariantSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    format = MovieFormatSerializer(allow_null=True)

    class Meta:
        model = MovieVariant
        fields = ['external_id', 'movie', 'format']
        extra_kwargs = {
            'external_id': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        movie = validated_data.get('movie')
        format = validated_data.pop('format')
        if format:
            format, created = MovieFormat.objects.update_or_create(**format)
            validated_data.update({'format': format})
        variant, created = MovieVariant.objects.update_or_create(external_id=validated_data.get('external_id'),
                                                                 defaults=validated_data)
        return variant
