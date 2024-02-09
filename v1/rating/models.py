#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete

from math import floor

from v1.recipe.models import Recipe


class Rating(models.Model):
    """
    Django Model to hold a Rating of a recipe.
    Ratings share a many to one relationship.
    Meaning each Recipe will have many Ratings.
    :recipe: = The recipe the comment is related to
    :comment: = A comment on the recipe
    :rating: = A rating 1-5
    :author: = User that created the comment
    :pub_date: = When the rating was created
    :update_author: = User that updated the comment
    :update_date: = When the rating was updated
    """
    recipe = models.ForeignKey(Recipe, related_name='rating_recipe', on_delete=models.CASCADE)
    comment = models.CharField(_('comment'), max_length=1000)
    rating = models.IntegerField(_('rating'), default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_author = models.ForeignKey(User, related_name='rating_update', on_delete=models.DO_NOTHING, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.rating, self.comment)

@receiver(post_save, sender=Rating)
def update_recipe_rating_on_save(sender, instance, **kwargs):
    recipe = getattr(instance, 'recipe')
    if recipe:
        update_recipe_rating(recipe)
    return

@receiver(post_delete, sender=Rating)
def update_recipe_rating_on_delete(sender, instance, **kwargs):
    recipe = getattr(instance, 'recipe')
    if recipe:
        update_recipe_rating(recipe)
    return

def update_recipe_rating(recipe=Recipe):
    ratings = Rating.objects.filter(recipe__id=recipe.id)
    rating_avg = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    recipe.rating = floor(rating_avg*10)/10 # floor to 1 decimal
    recipe.rating_count = ratings.count()
    recipe.save()
    return