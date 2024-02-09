#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework_bulk.serializers import BulkSerializerMixin, BulkListSerializer
from .models import GroceryList, GroceryItem


class GroceryItemSerializer(serializers.ModelSerializer):
    """Generic Serializer for grocery items"""
    class Meta:
        model = GroceryItem
        fields = [
            'id',
            'list',
            'title',
            'completed',
            'order',
        ]


class GroceryListSerializer(serializers.ModelSerializer):
    """
    Generic Serializer for grocery lists.
    This Serializer will also return the username
    of the user that owns the list.
    """
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    pub_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = GroceryList
        fields = [
            'id',
            'title',
            'slug',
            'item_count',
            'author',
            'pub_username',
            'pub_date',
        ]

    def create(self, validated_data):
        # Create the Grocery List.
        # Use the log-in user as the author.
        validated_data['author'] = self.context['request'].user
        return super(GroceryListSerializer, self).create(validated_data)


class BulkGroceryItemSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    Used to perform bulk operations on the GroceryItem model
    See: https://github.com/miki725/django-rest-framework-bulk
    """
    class Meta:
        model = GroceryItem
        list_serializer_class = BulkListSerializer
        fields = [
            'id',
            'list',
            'title',
            'completed',
            'order',
        ]
