# Generated by Django 3.2.6 on 2021-08-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_examdetail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdetail',
            name='slug',
            field=models.SlugField(max_length=164, unique=True),
        ),
    ]