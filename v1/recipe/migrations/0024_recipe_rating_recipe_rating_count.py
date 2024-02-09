# Generated by Django 4.1.9 on 2024-01-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0023_recipe_update_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='rating',
            field=models.FloatField(default=0, editable=False, help_text='calculated avg of ratings', verbose_name='rating avg'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='rating_count',
            field=models.IntegerField(default=0, editable=False, help_text='calculated number of ratings', verbose_name='rating count'),
        ),
    ]
