# Generated by Django 2.0.1 on 2018-01-29 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_mihai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='time',
            field=models.TimeField(),
        ),
    ]