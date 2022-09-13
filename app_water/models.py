
from django.db import models
from django_pandas.managers import DataFrameManager

class Meter_Category(models.Model):
	Category_Name = models.CharField(max_length=50)
	Category_Description = models.CharField(max_length=200, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Category_Name

	class Meta:
		ordering = ['Category_Name']

class Meter_Region(models.Model):
	Region_Name = models.CharField(max_length=50)
	Region_Description = models.CharField(max_length=200, blank=True, null=True)
	Region_Lat = models.CharField(max_length=20, blank=True, null=True)
	Region_Lng = models.CharField(max_length=20, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Region_Name

	class Meta:
		ordering = ['Region_Name']

class Meter_Type(models.Model):
    Type_Name = models.CharField(max_length=50)
    Type_Description = models.CharField(max_length=200, blank=True, null=True)
    Type_Make = models.CharField(max_length=50, blank=True, null=True)
    Type_Model = models.CharField(max_length=50, blank=True, null=True)
    Type_Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Type_Args = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Type_Name

    class Meta:
        ordering = ['Type_Name']

class Meter_List(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200, blank=True, null=True)
    Data_Table = models.CharField(max_length=50, blank=True, null=True)
    Start_Index = models.FloatField()
    Start_Date = models.DateTimeField('start date', blank=True, null=True)
    Pulse_Unit_Measurement = models.CharField(max_length=20, blank=True, null=True)
    Pulse_Unit_Value = models.FloatField()
    AppEUI = models.CharField(max_length=16, blank=True, null=True)
    DevEUI = models.CharField(max_length=16, blank=True, null=True)
    AppKey = models.CharField(max_length=32, blank=True, null=True)
    Lat = models.CharField(max_length=20, blank=True, null=True)
    Lng = models.CharField(max_length=20, blank=True, null=True)
    X = models.CharField(max_length=20, blank=True, null=True)
    Y = models.CharField(max_length=20, blank=True, null=True)
    Z = models.CharField(max_length=20, blank=True, null=True)
    Status =  models.IntegerField()
    Status_Description = models.CharField(max_length=200, blank=True, null=True)
    Type = models.ForeignKey(Meter_Type, on_delete=models.CASCADE)
    Region = models.ForeignKey(Meter_Region, on_delete=models.CASCADE)
    Category = models.ForeignKey(Meter_Category, on_delete=models.CASCADE)
    Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Args = models.CharField(max_length=200, blank=True, null=True)
    Last_Updated = models.DateTimeField('last updated', blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']

class Water_Meter(models.Model):
    Meter = models.ForeignKey(Meter_List, on_delete=models.CASCADE)
    Data_DateTime = models.DateTimeField('date published')
    Pulses = models.FloatField()
    Battery_Level = models.FloatField()
    Battery_Voltage = models.FloatField()

    objects = DataFrameManager()

    class Meta:
        ordering = ['Data_DateTime']

class Meter_Readings(models.Model):
    Meter_Id = models.ForeignKey(Meter_List, on_delete=models.CASCADE)
    Data_DateTime = models.DateTimeField('date published')
    Pulse_Count = models.IntegerField()
    Pulses = models.IntegerField()

    objects = DataFrameManager()

    class Meta:
        ordering = ['Data_DateTime']