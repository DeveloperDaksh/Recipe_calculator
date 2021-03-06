# Generated by Django 3.2.6 on 2021-10-12 12:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipesandingredients', '0029_alter_nutritiondetails_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritiondetails',
            name='protein',
            field=models.FloatField(default=2, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Must be greater than or equal to 0')]),
            preserve_default=False,
        ),
    ]
