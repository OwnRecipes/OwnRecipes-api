from django.core.management.base import BaseCommand

from v1.recipe.models import Recipe
from v1.rating.models import update_recipe_rating

class Command(BaseCommand):
    help = 'Calculates all recipes ratings (avg, count)'

    def handle(self, *args, **options):
        for recipe in Recipe.objects.all():
          update_recipe_rating(recipe)

        self.stdout.write(self.style.SUCCESS('Successfully updated recipe rating fields'))
