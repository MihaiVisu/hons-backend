# Generated by Django 2.0.1 on 2018-02-27 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_mihai', '0005_auto_20180203_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='lux_level',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='motion',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
    ]
