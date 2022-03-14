# Generated by Django 3.2.6 on 2021-08-27 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_alter_examdetail_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='educationdetails',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='educationdetails',
            constraint=models.UniqueConstraint(fields=('user', 'degree'), name='user_degree'),
        ),
        migrations.AddConstraint(
            model_name='examdetail',
            constraint=models.UniqueConstraint(fields=('name', 'exam_year'), name='unique_exam'),
        ),
    ]
