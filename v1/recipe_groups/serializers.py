#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from .models import Course, Cuisine, Season, Tag


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'author',
            'title',
        ]


class CuisineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Cuisine
        fields = [
            'id',
            'author',
            'title',
        ]


class SeasonSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    class Meta:
        model = Season
        fields = (
            'id',
            'title',
        )


class TagSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    class Meta:
        model = Tag
        fields = (
            'id',
            'title',
        )


class AggCourseSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class AggCuisineSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cuisine
        fields = '__all__'


class AggSeasonSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Season
        fields = '__all__'


class AggTagSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
