from django.db import models
from django_pandas.managers import DataFrameManager

class Kraken_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')
	Market = models.CharField(max_length=20)
	Open = models.FloatField()
	Close = models.FloatField()
	High = models.FloatField()
	Low = models.FloatField()
	Volume = models.FloatField()

	class Meta:
		ordering = ['Data_DateTime']