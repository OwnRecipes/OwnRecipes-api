#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Rating
from .models import Recipe


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe = serializers.SlugRelatedField(slug_field='slug', queryset=Recipe.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    pub_username = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.DateTimeField(read_only=True)
    update_author = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    update_username = serializers.ReadOnlyField(source='update_author.username')
    update_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id',
            'rating',
            'comment',
            'recipe',
            'author',
            'pub_username',
            'pub_date',
            'update_author',
            'update_username',
            'update_date',
        ]

    def create(self, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        validated_data['author'] = self.context['request'].user
        return super(RatingSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        validated_data['update_author'] = self.context['request'].user
        return super(RatingSerializer, self).update(instance, validated_data)

