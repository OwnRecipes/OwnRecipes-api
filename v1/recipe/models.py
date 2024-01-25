#!/usr/bin/env python
# encoding: utf-8

import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

from v1.common.db_fields import AutoSlugField
from v1.recipe_groups.models import Cuisine, Course, Tag

logger = logging.getLogger(__name__)

def _getImageQualityProcessors():
    if settings.RECIPE_IMAGE_QUALITY == 'HIGH':
        return [ResizeToFit(1920, 1440, False)]
    elif settings.RECIPE_IMAGE_QUALITY == 'MEDIUM':
        return [ResizeToFit(1440, 1080, False)]
    elif settings.RECIPE_IMAGE_QUALITY == 'LOW':
        return [ResizeToFit(1024, 768, False)]
    else: return None

def _getImageQualityOptions():
    if settings.RECIPE_IMAGE_QUALITY == 'HIGH':
        return {'quality': 97}
    elif settings.RECIPE_IMAGE_QUALITY == 'MEDIUM':
        return {'quality': 94}
    elif settings.RECIPE_IMAGE_QUALITY == 'LOW':
        return {'quality': 90}
    else: return None

class Recipe(models.Model):
    """
    Django Model to hold Recipes.

    Courses have a one to Many relation with Recipes.
    Cuisines have a one to Many relation with Recipes.
    Tags have a Many to Many relation with Recipes.
    Ingredient Groups have a Many to one relation with Recipes.
    Subrecipes have a Many to Many relation with Recipes.
        They allow another recipe to be show in the Ingredient section.

    :title: = Title of the Recipe
    :photo: = Raw Image of a Recipe
    :photo_thumbnail: = compressed image of the photo
    :info: = Description of the recipe
    :directions: = How to make the recipe
    :prep_time: = How long it takes to prepare the recipe
    :rating = avg of ratings. 0 if none.
    :cook_time: = How long the recipe takes to cook
    :servings: = How many people the recipe with serve
    :public: = If the recipe can be viewed by others
    :author: = Creator of the Recipe
    :pub_date: = When the recipe was created
    :update_author: = User that updated the recipe
    :update_date: = When the recipe was updated
    """
    title = models.CharField(_("Recipe Title"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    photo = ProcessedImageField(verbose_name='photo',
                                blank=True,
                                upload_to="upload/recipe_photos",
                                processors=_getImageQualityProcessors(),
                                format='JPEG',
                                options=_getImageQualityOptions())
    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(300, 200)],
                                     format='JPEG',
                                     options={'quality': 70})
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tag'), blank=True)
    subrecipes = models.ManyToManyField('self', verbose_name=_('subrecipes'), through='SubRecipe', symmetrical=False)
    info = models.TextField(_('info'), help_text="enter information about the recipe", blank=True)
    rating = models.FloatField(_('rating avg'), help_text="calculated avg of ratings", default=0, editable=False)
    directions = models.TextField(_('direction_text'), help_text="directions", blank=True)
    source = models.CharField(_('source'), max_length=200, blank=True)
    prep_time = models.IntegerField(_('prep time'), help_text="enter time in minutes", null=True, blank=True)
    cook_time = models.IntegerField(_('cook time'), help_text="enter time in minutes", null=True, blank=True)
    servings = models.IntegerField(_('servings'), help_text="enter total number of servings")
    public = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_author = models.ForeignKey(User, related_name='recipe_update', on_delete=models.DO_NOTHING, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.title

class SubRecipe(models.Model):
    numerator = models.FloatField(_('numerator'), default=0)
    denominator = models.FloatField(_('denominator'), default=1)
    measurement = models.TextField(_('measurement'), blank=True, null=True)
    child_recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name='child_recipe', null=True)
    parent_recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name='parent_recipe', null=True)

    def __str__(self):
        return '%s' % self.parent_recipe.title

# @see https://github.com/matthewwithanm/django-imagekit/issues/229
@receiver(post_delete, sender=Recipe)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    if not settings.DELETE_ORPHAN_FILES:
        return

    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field.name, instance_file_field)

""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    if not settings.DELETE_ORPHAN_FILES:
        return

    # Don't run on initial save
    if not instance.pk:
        return

    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance_in_db, field.name, instance_in_db_file_field)

""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, fieldname, instance_file_field):
    dynamic_field = {}
    dynamic_field[fieldname] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        delete_thumbnail(instance, fieldname + '_thumbnail')
        instance_file_field.delete(False)

def delete_thumbnail(instance, thumbnailFieldname):
    instance_thumbnail_field = getattr(instance, thumbnailFieldname)
    thumbnail_file = None
    try:
        thumbnail_file = instance_thumbnail_field.file
    except Exception as e:
        # It is just a thumbnail.
        # If there is none, or for some reason it can not be accessed,
        # we don't need to throw.
        logger.warning('Deletion of thumbnail failed. Could not get link to file.', exc_info=e)
        return

    try:
        cache_backend = instance_thumbnail_field.cachefile_backend
        cache_backend.cache.delete(cache_backend.get_key(thumbnail_file))
        instance_thumbnail_field.storage.delete(thumbnail_file.name)
    except Exception as e:
        logger.error('Deletion of thumbnail failed, file "' + thumbnail_file.name + '".', exc_info=e)
        pass
