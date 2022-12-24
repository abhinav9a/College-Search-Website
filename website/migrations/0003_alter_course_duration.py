from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20210801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
