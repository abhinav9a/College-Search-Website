# Generated by Django 3.2.6 on 2021-08-16 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_college_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='college',
            name='facilities',
        ),
        migrations.RemoveField(
            model_name='college',
            name='stream',
        ),
        migrations.AddField(
            model_name='college',
            name='facilities',
            field=models.ManyToManyField(null=True, to='website.Facilities'),
        ),
        migrations.AddField(
            model_name='college',
            name='stream',
            field=models.ManyToManyField(to='website.Stream'),
        ),
    ]
