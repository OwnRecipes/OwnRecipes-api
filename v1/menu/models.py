#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from v1.recipe.models import Recipe


class MenuItem(models.Model):
    """
    Django Model to hold a Recipe that is related to a menu.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False, blank=True)
    complete_date = models.DateTimeField(null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='menu_recipe', null=True)
    ext_title = models.CharField(_("External recipe Title"), max_length=250, blank=True)
    ext_source = models.CharField(_('source'), max_length=200, blank=True)

    def __str__(self):
        return '%s' % self.recipe.title
