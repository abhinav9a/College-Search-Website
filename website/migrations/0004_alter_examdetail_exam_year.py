# Generated by Django 3.2.7 on 2023-01-15 18:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_course_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdetail',
            name='exam_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1984), django.core.validators.MaxValueValidator(2024)]),
        ),
    ]