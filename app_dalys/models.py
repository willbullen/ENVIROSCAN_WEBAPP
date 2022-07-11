from django.db import models
from django_pandas.managers import DataFrameManager

class Node_Category(models.Model):
	Category_Name = models.CharField(max_length=50)
	Category_Description = models.CharField(max_length=200, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Category_Name

	class Meta:
		ordering = ['Category_Name']

class Node_Region(models.Model):
	Region_Name = models.CharField(max_length=50)
	Region_Description = models.CharField(max_length=200, blank=True, null=True)
	Region_Lat = models.CharField(max_length=20, blank=True, null=True)
	Region_Lng = models.CharField(max_length=20, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Region_Name

	class Meta:
		ordering = ['Region_Name']

class Node_Type(models.Model):
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

class Node_List(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200, blank=True, null=True)
    Data_Table = models.CharField(max_length=50, blank=True, null=True)
    Start_Index = models.FloatField(blank=True, null=True)
    Start_Date = models.DateTimeField('start date', blank=True, null=True)
    UUID = models.CharField(max_length=32, blank=True, null=True)    
    Pulse_Unit_Measurement = models.CharField(max_length=20, blank=True, null=True)
    Pulse_Unit_Value = models.FloatField(blank=True, null=True)
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
    Type = models.ForeignKey(Node_Type, on_delete=models.CASCADE)
    Region = models.ForeignKey(Node_Region, on_delete=models.CASCADE)
    Category = models.ForeignKey(Node_Category, on_delete=models.CASCADE)
    Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Args = models.CharField(max_length=200, blank=True, null=True)
    Last_Updated = models.DateTimeField('last updated', blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']

class Node_Water(models.Model):
    Node = models.ForeignKey(Node_List, on_delete=models.CASCADE)
    Data_DateTime = models.DateTimeField('date published')
    Pulses = models.FloatField()
    Battery_Level = models.FloatField()
    Battery_Voltage = models.FloatField()

    objects = DataFrameManager()

    class Meta:
        ordering = ['Data_DateTime']

class Node_Power(models.Model):
    Node = models.ForeignKey(Node_List, on_delete=models.CASCADE)
    Data_DateTime = models.DateTimeField('date published')
    RealPower_L1 = models.FloatField()
    RealPower_L2 = models.FloatField()
    RealPower_L3 = models.FloatField()
    AppaPower_L1 = models.FloatField()
    AppaPower_L2 = models.FloatField()
    AppaPower_L3 = models.FloatField()
    Irms_L1 = models.FloatField()
    Irms_L2 = models.FloatField()
    Irms_L3 = models.FloatField()
    Vrms_L1 = models.FloatField()
    Vrms_L2 = models.FloatField()
    Vrms_L3 = models.FloatField()
    PowerFact_L1 = models.FloatField()
    PowerFact_L2 = models.FloatField()
    PowerFact_L3 = models.FloatField()

    objects = DataFrameManager()

    class Meta:
        ordering = ['Data_DateTime']
