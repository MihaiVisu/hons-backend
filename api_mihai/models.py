from django.db import models

# Create your models here.


class CollectedData(models.Model):
    phone_timestamp = models.BigIntegerField()
    pm1 = models.DecimalField(max_digits=15, decimal_places=7)
    pm2_5 = models.DecimalField(max_digits=15, decimal_places=7)
    pm10 = models.DecimalField(max_digits=15, decimal_places=7)
    temperature = models.DecimalField(max_digits=15, decimal_places=7)
    humidity = models.DecimalField(max_digits=15, decimal_places=7)
    bin0 = models.IntegerField()
    bin1 = models.IntegerField()
    bin2 = models.IntegerField()
    bin3 = models.IntegerField()
    bin4 = models.IntegerField()
    bin5 = models.IntegerField()
    bin6 = models.IntegerField()
    bin7 = models.IntegerField()
    bin8 = models.IntegerField()
    bin9 = models.IntegerField()
    bin10 = models.IntegerField()
    bin11 = models.IntegerField()
    bin12 = models.IntegerField()
    bin13 = models.IntegerField()
    bin14 = models.IntegerField()
    bin15 = models.IntegerField()
    total = models.IntegerField()
    latitude = models.DecimalField(max_digits=15, decimal_places=7)
    longitude = models.DecimalField(max_digits=15, decimal_places=7)
    altitude = models.DecimalField(max_digits=15, decimal_places=7)
    accuracy = models.DecimalField(max_digits=15, decimal_places=7)
    time = models.TimeField()
    dataset = models.ForeignKey(
        'Dataset', blank=True, null=True, on_delete=models.CASCADE)


class Dataset(models.Model):
    name = models.CharField(max_length=50)
