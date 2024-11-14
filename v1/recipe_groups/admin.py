#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin
from .models import Course, Cuisine, Season, Tag


class CourseAndCuisineAndSeasonAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['author']


class TagAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['recipe__title']


admin.site.register(Course, CourseAndCuisineAndSeasonAdmin)
admin.site.register(Cuisine, CourseAndCuisineAndSeasonAdmin)
admin.site.register(Season, CourseAndCuisineAndSeasonAdmin)
admin.site.register(Tag, TagAdmin)
