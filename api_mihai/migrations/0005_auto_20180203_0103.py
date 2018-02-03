# Generated by Django 2.0.1 on 2018-02-03 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_mihai', '0004_auto_20180129_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeOfTransport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='accuracy',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='altitude',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='dataset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_mihai.Dataset'),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='transport_label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_mihai.ModeOfTransport'),
        ),
    ]
