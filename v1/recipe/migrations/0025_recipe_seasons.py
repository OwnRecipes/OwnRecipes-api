# Generated by Django 4.2.16 on 2024-11-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_groups', '0005_season'),
        ('recipe', '0024_recipe_rating_recipe_rating_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='seasons',
            field=models.ManyToManyField(blank=True, to='recipe_groups.season', verbose_name='season'),
        ),
    ]