# Generated by Django 2.0.1 on 2018-03-20 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_mihai', '0007_auto_20180227_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='phone_timestamp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
