#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from .models import Rating
from .models import Recipe


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe = serializers.SlugRelatedField(slug_field='slug', queryset=Recipe.objects.all())
    user_id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.DateTimeField(read_only=True)
    update_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id',
            'rating',
            'comment',
            'recipe',
            'user_id',
            'username',
            'author',
            'pub_date',
            'update_date'
        ]

    def update(self, instance, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        return super(RatingSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        return super(RatingSerializer, self).create(validated_data)
