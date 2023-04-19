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

class Node_Temperature(models.Model):
    Node = models.ForeignKey(Node_List, on_delete=models.CASCADE)
    Data_DateTime = models.DateTimeField('date published')
    Battery_MV = models.FloatField()
    Battery_Percent = models.FloatField()
    Temperature = models.FloatField()

    objects = DataFrameManager()

    class Meta:
        ordering = ['Data_DateTime']



#########################################
######## 3D REPORTS
class Reports_Scans(models.Model):
    Scan_Name = models.CharField(max_length=50)
    Scan_PID = models.CharField(max_length=50, blank=True, null=True)
    Scan_Value = models.CharField(max_length=50, blank=True, null=True)
    Scan_Title = models.CharField(max_length=50, blank=True, null=True)
    Scan_Xpos = models.CharField(max_length=50, blank=True, null=True)
    Scan_Zpos = models.CharField(max_length=50, blank=True, null=True)
    Scan_Show =  models.IntegerField(blank=True, null=True)
    Scan_Color = models.CharField(max_length=50, blank=True, null=True)
    Scan_Number =  models.IntegerField(blank=True, null=True)
    Scan_Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Scan_Args = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Scan_Name

    class Meta:
        ordering = ['Scan_Name']

class Reports_Levels(models.Model):
    Level_Name = models.CharField(max_length=50)
    Level_ID =  models.IntegerField(blank=True, null=True)
    Level_LevelImagePath = models.CharField(max_length=50, blank=True, null=True)
    Level_xOffset = models.FloatField(blank=True, null=True)
    Level_xConst = models.FloatField(blank=True, null=True)
    Level_zOffset = models.FloatField(blank=True, null=True)
    Level_zConst = models.FloatField(blank=True, null=True)
    Level_meXOffset = models.FloatField(blank=True, null=True)
    Level_meXConst = models.FloatField(blank=True, null=True)
    Level_meZOffset = models.FloatField(blank=True, null=True)
    Level_meZConst = models.FloatField(blank=True, null=True)
    Level_Rotate = models.IntegerField(blank=True, null=True)
    Level_FlipMe = models.IntegerField(blank=True, null=True)
    Scan = models.ForeignKey(Reports_Scans, on_delete=models.CASCADE)
    Level_Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Level_Args = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Level_Name

    class Meta:
        ordering = ['Level_Name']

class Reports_Models(models.Model):
    Model_Name = models.CharField(max_length=50)
    Model_MportID = models.CharField(max_length=200, blank=True, null=True)
    Model_DateTime = models.DateTimeField('date published')
    Level = models.ForeignKey(Reports_Levels, on_delete=models.CASCADE)
    Model_Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Model_Args = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Model_Name

    class Meta:
        ordering = ['Model_Name']

class Reports_Project(models.Model):
    Project_Name = models.CharField(max_length=50)
    Project_Description = models.CharField(max_length=200, blank=True, null=True)
    Project_Status =  models.IntegerField()
    Model = models.ForeignKey(Reports_Models, on_delete=models.CASCADE, blank=True, null=True)
    Project_Kwargs = models.CharField(max_length=200, blank=True, null=True)
    Project_Args = models.CharField(max_length=200, blank=True, null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.Project_Name

    class Meta:
        ordering = ['Project_Name']