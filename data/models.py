from django.db import models
from django_pandas.managers import DataFrameManager

class Aethalometer_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')
	Data_Serial_Number = models.CharField(max_length=20)
	Data_BC1 = models.FloatField()
	Data_BC2 = models.FloatField()
	Data_BC3 = models.FloatField()
	Data_BC4 = models.FloatField()
	Data_BC5 = models.FloatField()
	Data_BC6 = models.FloatField()
	Data_BC7 = models.FloatField()
	Data_FlowC = models.FloatField()
	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	class Meta:
		ordering = ['Data_DateTime']

class Aethalometer_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	class Meta:
		ordering = ['Log_DateTime']







class Picarro_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')	
	Data_CO2 = models.FloatField()
	Data_CO2_Dry = models.FloatField()
	Data_CO = models.FloatField()
	Data_CH4 = models.FloatField()
	Data_CH4_Dry = models.FloatField()
	Data_H2O = models.FloatField()
	Data_Amb_P = models.FloatField()
	Data_CavityPressure = models.FloatField()
	Data_Cavity_Temp = models.FloatField()
	Data_DasTemp = models.FloatField()
	Data_EtalonTemp = models.FloatField()
	Data_WarmBoxTemp = models.FloatField()
	Data_Species = models.FloatField()
	Data_MPVPosition = models.FloatField()
	Data_OutletValve = models.FloatField()
	Data_Solenoid_Valves = models.FloatField()
	Data_h2o_reported = models.FloatField()
	Data_b_h2o_pct = models.FloatField()
	Data_peak_14 = models.FloatField()
	Data_peak84_raw = models.FloatField()
	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Picarro_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Log_DateTime']

#class Picarro_Anomalies(models.Model):
#	Anomaly_DateTime = models.DateTimeField('date published')
#	Anomaly_Node_Id = models.IntegerField()
#	Anomaly_Data_Id = models.IntegerField()
#	Anomaly_Property_Id = models.IntegerField()
#	Anomaly_Details = models.CharField(max_length=200)
#
#	objects = DataFrameManager()
#
#	class Meta:
#		ordering = ['Anomaly_DateTime']

class Picarro_Alarms(models.Model):
	Alarms_DateTime = models.DateTimeField('date published')
	Alarms_Type = models.IntegerField()
	Alarms_Details = models.CharField(max_length=200)
	Alarms_Acknowledged = models.BooleanField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Alarms_DateTime']

class Picarro_PM(models.Model):
	PM_DateCreated = models.DateTimeField('date published')
	PM_Title = models.CharField(max_length=100)
	PM_Type = models.IntegerField()
	PM_Time_Interval = models.IntegerField()
	PM_Details = models.CharField(max_length=200, blank=True, null=True)

	PM_Task = models.CharField(max_length=100, blank=True, null=True)
	PM_Kwargs = models.CharField(max_length=200, blank=True, null=True)
	PM_Args = models.CharField(max_length=200, blank=True, null=True)
	PM_Enabled = models.IntegerField(0)
	PM_Last_Run_At = models.DateTimeField(blank=True, null=True)
	PM_Total_Run_Count = models.IntegerField(0)
	PM_Date_Changed = models.DateTimeField(blank=True, null=True)
	PM_One_Off = models.IntegerField(0)

	objects = DataFrameManager()

	class Meta:
		ordering = ['PM_DateCreated']

class Picarro_Jobs(models.Model):
	Jobs_DateCreated = models.DateTimeField('date published')
	Jobs_DateToBeCompleted = models.DateTimeField(blank=True, null=True)
	Jobs_DateCompleted = models.DateTimeField(blank=True, null=True)
	Jobs_Title = models.CharField(max_length=100)
	Jobs_Description = models.CharField(max_length=400, blank=True, null=True)
	Jobs_Notes = models.CharField(max_length=200, blank=True, null=True)
	Jobs_Type = models.IntegerField()
	Jobs_Status = models.IntegerField()
	PM = models.ForeignKey(Picarro_PM, on_delete=models.CASCADE, blank=True, null=True)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Jobs_DateCreated']

class Picarro_Property_Types(models.Model):
	Properties_Type_Name = models.CharField(max_length=100)	

	objects = DataFrameManager()

class Picarro_Properties(models.Model):
	Properties_DateCreated = models.DateTimeField('date published')
	Properties_Type = models.IntegerField()
	#Properties_Type = models.ForeignKey(Picarro_Property_Types, on_delete=models.CASCADE, blank=True, null=True)
	Properties_Title = models.CharField(max_length=100)
	Properties_Value = models.IntegerField()
	Properties_Kwargs = models.CharField(max_length=200, blank=True, null=True)
	Properties_Args = models.CharField(max_length=200, blank=True, null=True)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Properties_DateCreated']


class Defib_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published', blank=True, null=True)
	Defib_Id = models.IntegerField(blank=True, null=True)
	Temperature = models.FloatField(blank=True, null=True)
	Humidity = models.FloatField(blank=True, null=True)
	Pressure = models.FloatField(blank=True, null=True)
	Battery = models.FloatField(blank=True, null=True)

	class Meta:
		ordering = ['Data_DateTime']


























class Weather_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')
	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_MaxGustTime = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindDirFlag = models.FloatField()
	Data_WindSpeed = models.FloatField()
	Data_WindSpeedFlag = models.FloatField()
	Data_WindSpeed_Min = models.FloatField()
	Data_WindSpeed_StdDev = models.FloatField()
	Data_Characteristic = models.FloatField()
	Data_Pressure = models.FloatField()
	Data_PressureFlag = models.FloatField()
	Data_Tendency = models.FloatField()
	Data_DryA = models.FloatField()
	Data_DryA_Flag = models.FloatField()
	Data_GrassA = models.FloatField()
	Data_GrassA_Flag = models.FloatField()
	Data_HumA = models.FloatField()
	Data_HumA_Flag = models.FloatField()
	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Weather_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	class Meta:
		ordering = ['Log_DateTime']

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

class Tucson_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')
	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_MaxGustTime = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindDirFlag = models.FloatField()
	Data_WindSpeed = models.FloatField()
	Data_WindSpeedFlag = models.FloatField()
	Data_WindSpeed_Min = models.FloatField()
	Data_WindSpeed_StdDev = models.FloatField()
	Data_DryA = models.FloatField()
	Data_GrassA = models.FloatField()
	Data_5cmA = models.FloatField()
	Data_10cmA = models.FloatField()
	Data_20cmA = models.FloatField()
	Data_30cmA = models.FloatField()
	Data_50cmA = models.FloatField()
	Data_100cmA = models.FloatField()
	Data_HumA = models.FloatField()
	Data_SolarRadA = models.FloatField()
	Data_Characteristic = models.FloatField()
	Data_Pressure = models.FloatField()
	Data_Tendency = models.FloatField()
	Data_VisAlarm = models.FloatField()
	Data_HardwareError = models.FloatField()
	Data_OneMinVis = models.FloatField()
	Data_TenMinVis = models.FloatField()
	Data_PWCode_Int = models.FloatField()
	Data_PWCode15 = models.FloatField()
	Data_PWCodeHour = models.FloatField()
	Data_Intensity = models.FloatField()
	Data_Water = models.FloatField()
	Data_Snow = models.FloatField()
	Data_DayOfYear = models.FloatField()
	Data_CMP11_MinGlobal = models.FloatField()
	Data_CSD3_MinSunshine = models.FloatField()
	Data_SPN1_MinSunshine = models.FloatField()
	Data_SPN1_MinGlobal = models.FloatField()
	Data_SPN1_MinDiffuse = models.FloatField()

	class Meta:
		ordering = ['Data_DateTime']

class Tucson_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	class Meta:
		ordering = ['Log_DateTime']

class Baloon_Data(models.Model):
	Data_DateTime = models.DateTimeField('date published')
	Data_Height = models.FloatField()

	class Meta:
		ordering = ['Data_DateTime']

class Baloon_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	class Meta:
		ordering = ['Log_DateTime']