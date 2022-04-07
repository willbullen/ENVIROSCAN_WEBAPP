from django.db import models
from django_pandas.managers import DataFrameManager
from django.contrib.auth.models import User

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













######################################################
################# MET EIREANN MODELS #################
######################################################

class Clients(models.Model):
	Client_Name = models.CharField(max_length=50)
	Client_Description = models.CharField(max_length=200, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Client_Name

	class Meta:
		ordering = ['Client_Name']

class Node_Category(models.Model):
	Category_Name = models.CharField(max_length=50)
	Category_Description = models.CharField(max_length=200, blank=True, null=True)
	Client = models.ForeignKey(Clients, on_delete=models.CASCADE)

	objects = DataFrameManager()

	def __str__(self):
		return self.Category_Name

	class Meta:
		ordering = ['Category_Name']

class Node_Location(models.Model):
	Location_Name = models.CharField(max_length=50)
	Location_Description = models.CharField(max_length=200, blank=True, null=True)
	Location_Lat = models.CharField(max_length=20, blank=True, null=True)
	Location_Lng = models.CharField(max_length=20, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Location_Name

	class Meta:
		ordering = ['Location_Name']

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

class Nodes(models.Model):
	Node_ID = models.CharField(max_length=20)
	Node_Name = models.CharField(max_length=50)
	Node_Description = models.CharField(max_length=200, blank=True, null=True)
	Node_Ip = models.CharField(max_length=20, blank=True, null=True)
	Node_Device_ID = models.CharField(max_length=50, blank=True, null=True)
	Asset_Ip = models.CharField(max_length=20, blank=True, null=True)
	Node_Lat = models.CharField(max_length=20, blank=True, null=True)
	Node_Lng = models.CharField(max_length=20, blank=True, null=True)
	Node_X = models.CharField(max_length=20, blank=True, null=True)
	Node_Y = models.CharField(max_length=20, blank=True, null=True)
	Node_Z = models.CharField(max_length=20, blank=True, null=True)
	Status =  models.IntegerField()
	Asset_Status =  models.IntegerField()
	Asset_Status_Description = models.CharField(max_length=200, blank=True, null=True)
	Node_Status =  models.IntegerField()
	Node_Status_Description = models.CharField(max_length=200, blank=True, null=True)
	Server_Status =  models.IntegerField()
	Server_Status_Description = models.CharField(max_length=200, blank=True, null=True)
	Type = models.ForeignKey(Node_Type, on_delete=models.CASCADE)
	Location = models.ForeignKey(Node_Location, on_delete=models.CASCADE)
	Client = models.ForeignKey(Clients, on_delete=models.CASCADE)
	Category = models.ForeignKey(Node_Category, on_delete=models.CASCADE)

	objects = DataFrameManager()

	def __str__(self):
		return self.Node_ID

	class Meta:
		ordering = ['Node_ID']

#########   PICARRO G2401  ##########
class Picarro_Data(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
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

	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindSpeed = models.FloatField()	
	Data_Pressure = models.FloatField()	
	Data_DryA = models.FloatField()	
	Data_GrassA = models.FloatField()	
	Data_HumA = models.FloatField()	

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

#################### NOX ######################
class NOX_Data(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')	
	Data_Box_Temp = models.FloatField()
	Data_HVPS = models.FloatField()
	Data_NO_Conc = models.FloatField()
	Data_NO_Norm_Offset = models.FloatField()
	Data_NO_Slope = models.FloatField()
	Data_NO_Stability = models.FloatField()
	Data_NO2_Conc = models.FloatField()
	Data_NO2_Stability = models.FloatField()
	Data_Norm_PMT = models.FloatField()
	Data_NOX_Conc = models.FloatField()
	Data_NOx_Norm_Offset = models.FloatField()
	Data_NOx_Slope = models.FloatField()
	Data_NOX_Stability = models.FloatField()
	Data_PMT_Signal = models.FloatField()
	Data_PMT_Temp = models.FloatField()
	Data_Ref_4096mV = models.FloatField()
	Data_Ref_Ground = models.FloatField()
	Data_Rx_Cell_Press = models.FloatField()
	Data_Rx_Cell_Temp = models.FloatField()
	Data_Sample_Flow = models.FloatField()
	
	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindSpeed = models.FloatField()	
	Data_Pressure = models.FloatField()	
	Data_DryA = models.FloatField()	
	Data_GrassA = models.FloatField()	
	Data_HumA = models.FloatField()	

	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

#################### SOX ######################
class SOX_Data(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')	
	Data_Box_Temp = models.FloatField()
	Data_HVPS = models.FloatField()
	Data_Lamp_Dark = models.FloatField()
	Data_Lamp_Ratio = models.FloatField()
	Data_Norm_PMT = models.FloatField()
	Data_Photo_Absolute = models.FloatField()
	Data_PMT = models.FloatField()
	Data_PMT_Dark = models.FloatField()
	Data_PMT_Signal = models.FloatField()
	Data_PMT_Temp = models.FloatField()
	Data_Sox_Pressure = models.FloatField()
	Data_RCell_Temp = models.FloatField()
	Data_Ref_4096mV = models.FloatField()
	Data_Ref_Ground = models.FloatField()
	Data_REF_V_4096_Dark = models.FloatField()
	Data_REF_V_4096_Light = models.FloatField()
	Data_Sample_Flow = models.FloatField()
	Data_SO2_Concentration = models.FloatField()
	Data_Stability = models.FloatField()
	Data_UV_Lamp = models.FloatField()

	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindSpeed = models.FloatField()	
	Data_Pressure = models.FloatField()	
	Data_DryA = models.FloatField()	
	Data_GrassA = models.FloatField()	
	Data_HumA = models.FloatField()	

	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

#################### AUTOSONDE ######################

class Autosonde_Soundings(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_Day = models.DateTimeField('date published')
	Data_Type = models.CharField(max_length=5, blank=True, null=True)
	Data_Stage_1 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_2 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_3 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_4 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_5 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_6 = models.DateTimeField('date published', blank=True, null=True)
	Data_Stage_7 = models.DateTimeField('date published', blank=True, null=True)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_Day']

class Autosonde_Sounding_Data(models.Model):
	Sounding_ID = models.ForeignKey(Autosonde_Soundings, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')
	Data_EVSS = models.FloatField()
	Data_Pressure = models.FloatField()
	Data_Geopotential_Height = models.FloatField()
	Data_Lat = models.FloatField()
	Data_Lng = models.FloatField()
	Data_Air_Temperature = models.FloatField()
	Data_Dewpoint_Temperature = models.FloatField()
	Data_Direction = models.FloatField()
	Data_Speed = models.FloatField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Autosonde_Logs(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Log_DateTime']

class Autosonde_Ground_Station(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')
	Met_Gust_Max = models.FloatField()
	Met_Gust_Direction = models.FloatField()
	Met_Wind_Direction = models.FloatField()
	Met_Wind_Speed = models.FloatField()	
	Met_Pressure = models.FloatField()	
	Met_Temperature_Dry = models.FloatField()	
	Met_Temperature_Grass = models.FloatField()	
	Met_Humidity = models.FloatField()
	Station_Supply_Voltage = models.FloatField()
	Station_Supply_L1 = models.FloatField()
	Station_Supply_L2 = models.FloatField()
	Station_Supply_L3 = models.FloatField()
	Station_UPS_Battery_Level = models.FloatField()
	Station_UPS_Battery_Voltage = models.FloatField()
	Station_UPS_Est_Run_Time = models.FloatField()
	Station_UPS_Frequency = models.FloatField()
	Station_UPS_Load = models.FloatField()
	Station_UPS_Status = models.IntegerField()
	Station_UPS_Output_Voltage = models.FloatField()
	Station_UPS_Temperature = models.FloatField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

##################### TUCSON #######################

class Tucson_Data(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
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
	
	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Tucson_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Log_DateTime']

################ AETHALOMETER #####################

class Aethalometer_Data(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
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

	Data_MaxGust = models.FloatField()
	Data_MaxGustDir = models.FloatField()
	Data_WindDir = models.FloatField()
	Data_WindSpeed = models.FloatField()	
	Data_Pressure = models.FloatField()	
	Data_DryA = models.FloatField()	
	Data_GrassA = models.FloatField()	
	Data_HumA = models.FloatField()	

	Instrument_Supply_Voltage = models.FloatField()
	Instrument_Supply_Current = models.FloatField()
	Instrument_Temp = models.FloatField()
	Instrument_Pressure = models.FloatField()
	Instrument_Humidity = models.FloatField()
	Instrument_Status = models.IntegerField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Aethalometer_Logs(models.Model):
	Log_DateTime = models.DateTimeField('date published')
	Log_Type = models.IntegerField()
	Log_Details = models.CharField(max_length=200)

	objects = DataFrameManager()

	class Meta:
		ordering = ['Log_DateTime']

class UPS(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')
	Supply_Voltage = models.FloatField()
	Supply_L1 = models.FloatField()
	Supply_L2 = models.FloatField()
	Supply_L3 = models.FloatField()
	UPS_Battery_Level = models.FloatField()
	UPS_Battery_Voltage = models.FloatField()
	UPS_Est_Run_Time = models.FloatField()
	UPS_Frequency = models.FloatField()
	UPS_Load = models.FloatField()
	UPS_Status = models.IntegerField()
	UPS_Output_Voltage = models.FloatField()
	UPS_Temperature = models.FloatField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']

class Generator(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Data_DateTime = models.DateTimeField('date published')
	Generator_Voltage = models.FloatField()
	Generator_L1 = models.FloatField()
	Generator_L2 = models.FloatField()
	Generator_L3 = models.FloatField()
	Generator_Battery_Level = models.FloatField()
	Generator_Battery_Voltage = models.FloatField()
	Generator_Frequency = models.FloatField()
	Generator_Load = models.FloatField()
	Generator_Status = models.IntegerField()
	Generator_Output_Voltage = models.FloatField()
	Generator_Oil_Temperature = models.FloatField()
	Generator_Coolent_Temperature = models.FloatField()
	Generator_Oil_Pressure = models.FloatField()
	Generator_Fuel_Level = models.FloatField()
	Generator_Running_Hours = models.FloatField()

	objects = DataFrameManager()

	class Meta:
		ordering = ['Data_DateTime']


######################################################
################# CMMS SYSTEM MODELS #################
######################################################

class CMMS_Job_Types(models.Model):	
	Job_Type_Title = models.CharField(max_length=100)
	Job_Type_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Type_Title

	class Meta:
		ordering = ['Job_Type_Title']

class CMMS_Job_Status(models.Model):	
	Job_Status_Title = models.CharField(max_length=100)
	Job_Status_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Status_Title

	class Meta:
		ordering = ['Job_Status_Title']

class CMMS_Job_Task_Status(models.Model):	
	Job_Task_Status_Title = models.CharField(max_length=100)
	Job_Task_Status_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Task_Status_Title

	class Meta:
		ordering = ['Job_Task_Status_Title']

class CMMS_Job_Priority(models.Model):	
	Job_Priority_Title = models.CharField(max_length=100)
	Job_Priority_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Priority_Title

	class Meta:
		ordering = ['Job_Priority_Title']

class CMMS_Job_Schedule_Type(models.Model):	
	Job_Schedule_Type_Title = models.CharField(max_length=100)
	Job_Schedule_Type_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Schedule_Type_Title

	class Meta:
		ordering = ['Job_Schedule_Type_Title']

class CMMS_Job_Schedule_Period(models.Model):	
	Job_Schedule_Period = models.CharField(max_length=100)
	Job_Schedule_Period_Description = models.CharField(max_length=500, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Schedule_Period

	class Meta:
		ordering = ['Job_Schedule_Period']

class CMMS_Jobs(models.Model):
	Node_ID = models.ForeignKey(Nodes, on_delete=models.CASCADE)
	Author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
	Job_Created_DateTime = models.DateTimeField('date published')
	Job_Title = models.CharField(max_length=100)
	Job_Description = models.CharField(max_length=500, blank = True, null = True)
	Job_Start_Date = models.DateTimeField('start date', blank = True, null = True)
	Job_End_Date = models.DateTimeField('end date', blank = True, null = True)
	Job_Type = models.ForeignKey(CMMS_Job_Types, on_delete=models.CASCADE)
	Job_Status = models.ForeignKey(CMMS_Job_Status, on_delete=models.CASCADE)
	Job_Priority = models.ForeignKey(CMMS_Job_Priority, on_delete=models.CASCADE)
	Job_Schedule_Type = models.ForeignKey(CMMS_Job_Schedule_Type, on_delete=models.CASCADE, blank = True, null = True)
	Job_Schedule_Period = models.ForeignKey(CMMS_Job_Schedule_Period, on_delete=models.CASCADE, blank = True, null = True)
	Job_Schedule_Period_Value = models.IntegerField(blank = True, null = True)
	Job_Completed_Date = models.DateTimeField('date completed', blank = True, null = True)
	Job_Completed_Comments = models.CharField(max_length=1000, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Title

	class Meta:
		ordering = ['Job_Created_DateTime']

class CMMS_Job_Tasks(models.Model):	
	Job = models.ForeignKey(CMMS_Jobs, related_name = 'Tasks', on_delete=models.CASCADE)
	Job_Task_Title = models.CharField(max_length=100)
	Job_Task_Description = models.CharField(max_length=500, blank = True, null = True)
	Job_Task_Status = models.ForeignKey(CMMS_Job_Task_Status, on_delete=models.CASCADE, blank = True, null = True)
	Job_Task_Completed_Date = models.DateTimeField('date completed', blank = True, null = True)
	Job_Task_Completed_Comments = models.CharField(max_length=1000, blank = True, null = True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Task_Title

	class Meta:
		ordering = ['Job_Task_Title']

class CMMS_Job_Attachments(models.Model):	
	Job = models.ForeignKey(CMMS_Jobs, on_delete=models.CASCADE)
	Job_Attachment_Title = models.CharField(max_length=100)
	Job_Attachment_Description = models.CharField(max_length=500, blank = True, null = True)
	Job_Attachment_Filepath = models.FileField(upload_to = 'files/', null = True, verbose_name = "")

	objects = DataFrameManager()

	def __str__(self):
		return self.Job_Attachment_Title

	class Meta:
		ordering = ['Job_Attachment_Title']	