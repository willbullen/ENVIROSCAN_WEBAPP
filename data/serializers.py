from rest_framework import serializers
from .models import Defib_Data, Aethalometer_Data, Aethalometer_Logs, Picarro_Data, Picarro_Logs, Weather_Data, Weather_Logs, Kraken_Data, Tucson_Data, Tucson_Logs, Baloon_Data, Baloon_Logs, Picarro_PM, Picarro_Jobs, Picarro_Properties, Picarro_Alarms, Picarro_Property_Types

class Aethalometer_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aethalometer_Data
        fields = [
            'id', 
            'Data_DateTime',
            'Data_Serial_Number',
            'Data_BC1',
            'Data_BC2',
            'Data_BC3',
            'Data_BC4', 
            'Data_BC5', 
            'Data_BC6', 
            'Data_BC7', 
            'Data_FlowC', 
            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Aethalometer_Logs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aethalometer_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Picarro_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Data
        fields = [
            'id', 
            'Data_DateTime',
            'Data_CO2',
            'Data_CO2_Dry',
            'Data_CO',
            'Data_CH4',
            'Data_CH4_Dry',
            'Data_H2O',
            'Data_Amb_P',
            'Data_CavityPressure',
            'Data_Cavity_Temp',
            'Data_DasTemp',
            'Data_EtalonTemp',
            'Data_WarmBoxTemp',
            'Data_Species',
            'Data_MPVPosition',
            'Data_OutletValve',
            'Data_Solenoid_Valves',
            'Data_h2o_reported',
            'Data_b_h2o_pct',
            'Data_peak_14',
            'Data_peak84_raw',
            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Picarro_Logs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Picarro_Alarms_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Alarms
        fields = [
            'id',
            'Alarms_DateTime',
            'Alarms_Type',
            'Alarms_Details',
            'Alarms_Acknowledged',
        ]

class Picarro_PM_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_PM
        fields = [
            'id',
            'PM_DateCreated',
            'PM_Title',
            'PM_Type',
            'PM_Time_Interval',
            'PM_Details',
            'PM_Task',
            'PM_Kwargs',
            'PM_Args',
            'PM_Enabled',
            'PM_Last_Run_A',
            'PM_Total_Run_Count',
            'PM_Date_Changed',
            'PM_One_Off',
        ]

class Picarro_Jobs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Jobs
        fields = [
            'id',
            'Jobs_DateCreated',
            'Jobs_DateToBeCompleted',
            'Jobs_DateCompleted',
            'Jobs_Title',
            'Jobs_Description',
            'Jobs_Notes',
            'Jobs_Type',
            'Jobs_Status',
            'PM',
        ]

class Picarro_Properties_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Properties
        fields = [
            'id',
            'Properties_DateCreated',
            'Properties_Type',
            'Properties_Title',
            'Properties_Value',
            'Properties_Kwargs',
            'Properties_Args'
        ]

class Picarro_Property_Types_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picarro_Property_Types
        fields = [
            'id',
            'Properties_Type_Name'
        ]


class Defib_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Defib_Data
        fields = [
            'id',
            'Defib_Id',
            'Temperature',
            'Humidity',
            'Pressure',
            'Battery',
        ]






class Weather_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather_Data
        fields = [
            'id', 
            'Data_DateTime',
            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_MaxGustTime',
            'Data_WindDir',
            'Data_WindDirFlag',
            'Data_WindSpeed',
            'Data_WindSpeedFlag',
            'Data_WindSpeed_Min',
            'Data_WindSpeed_StdDev',
            'Data_Characteristic',
            'Data_Pressure',
            'Data_PressureFlag',
            'Data_Tendency',
            'Data_DryA',
            'Data_DryA_Flag',
            'Data_GrassA',
            'Data_GrassA_Flag',
            'Data_HumA',
            'Data_HumA_Flag',            
            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Weather_Logs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Kraken_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kraken_Data
        fields = [
            'id', 
            'Data_DateTime', 
            'Market',
            'Open',
            'Close',
            'High',
            'Low',
            'Volume',
        ]

class Tucson_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tucson_Data
        fields = [
            'id', 
            'Data_DateTime',
            # ---- Tbl_WLog_01_Wind_A ----
            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_MaxGustTime',
            'Data_WindDir',
            'Data_WindDirFlag',
            'Data_WindSpeed',
            'Data_WindSpeedFlag',
            'Data_WindSpeed_Min',
            'Data_WindSpeed_StdDev',
            # ---- Tbl_01_Pres_A ----
            'Data_Characteristic',
            'Data_Pressure',
            'Data_Tendency',
            # ---- Tbl_01_Suit_A ----
            'Data_DryA',
            'Data_GrassA',
            'Data_5cmA',
            'Data_10cmA',
            'Data_20cmA',
            'Data_30cmA',
            'Data_50cmA',
            'Data_100cmA',
            'Data_HumA',
            'Data_SolarRadA',
            # ---- PW-S ----
            'Data_VisAlarm',
            'Data_HardwareError',
            'Data_OneMinVis',
            'Data_TenMinVis',
            'Data_PWCode_Int',
            'Data_PWCode15',
            'Data_PWCodeHour',
            'Data_Intensity',
            'Data_Water',
            'Data_Snow',
            # ---- S BAND RADAR ----
            'Data_DayOfYear',
            'Data_CMP11_MinGlobal',
            'Data_CSD3_MinSunshine',
            'Data_SPN1_MinSunshine',
            'Data_SPN1_MinGlobal',
            'Data_SPN1_MinDiffuse',
        ]

class Tucson_Logs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tucson_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Baloon_Data_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Baloon_Data
        fields = [
            'id', 
            'Data_DateTime',            
            'Data_Height',
        ]

class Baloon_Logs_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Baloon_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]