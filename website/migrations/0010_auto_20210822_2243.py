# Generated by Django 3.2.6 on 2021-08-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_college_college_ranking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-published_on']},
        ),
    ]
