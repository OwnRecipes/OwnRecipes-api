#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin
from .models import Course, Cuisine, Season, Tag


class CourseAndCuisineAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['author']


class TagAndSeasonAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['recipe__title']


admin.site.register(Course, CourseAndCuisineAdmin)
admin.site.register(Cuisine, CourseAndCuisineAdmin)
admin.site.register(Season, TagAndSeasonAdmin)
admin.site.register(Tag, TagAndSeasonAdmin)
