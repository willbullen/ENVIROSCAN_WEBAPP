from rest_framework import serializers
from .models import UPS, Generator, Autosonde_Ground_Station, Autosonde_Logs, Autosonde_Sounding_Data, Autosonde_Soundings, Node_Category, Clients, NOX_Data, Node_Location, Node_Type, Nodes, SOX_Data, Defib_Data, Aethalometer_Data, Aethalometer_Logs, Picarro_Data, Picarro_Logs, Weather_Data, Weather_Logs, Kraken_Data, Tucson_Data, Tucson_Logs, Baloon_Data, Baloon_Logs, Picarro_PM, Picarro_Jobs, Picarro_Properties, Picarro_Alarms, Picarro_Property_Types

class Aethalometer_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aethalometer_Data
        fields = [
            'id',
            'Node_ID', 
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
            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_WindDir',
            'Data_WindSpeed',	
            'Data_Pressure',
            'Data_DryA',
            'Data_GrassA',
            'Data_HumA',
            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Aethalometer_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aethalometer_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Picarro_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Picarro_Data
        fields = [
            'id', 
            'Node_ID',
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

            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_WindDir',
            'Data_WindSpeed',	
            'Data_Pressure',
            'Data_DryA',
            'Data_GrassA',
            'Data_HumA',

            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Picarro_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Picarro_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Picarro_Alarms_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Picarro_Alarms
        fields = [
            'id',
            'Alarms_DateTime',
            'Alarms_Type',
            'Alarms_Details',
            'Alarms_Acknowledged',
        ]

class Picarro_PM_Serializer(serializers.ModelSerializer):
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

class Picarro_Jobs_Serializer(serializers.ModelSerializer):
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

class Picarro_Properties_Serializer(serializers.ModelSerializer):
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

class Picarro_Property_Types_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Picarro_Property_Types
        fields = [
            'id',
            'Properties_Type_Name'
        ]


class Defib_Data_Serializer(serializers.ModelSerializer):
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






class Weather_Data_Serializer(serializers.ModelSerializer):
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

class Weather_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Weather_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Kraken_Data_Serializer(serializers.ModelSerializer):
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

class Tucson_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tucson_Data
        fields = [
            'id', 
            'Node_ID',
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

class Tucson_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tucson_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Baloon_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Baloon_Data
        fields = [
            'id', 
            'Data_DateTime',            
            'Data_Height',
        ]

class Baloon_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Baloon_Logs
        fields = [
            'id',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class SOX_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SOX_Data
        fields = [
            'id', 
            'Node_ID',
            'Data_DateTime',
            'Data_Box_Temp',
            'Data_HVPS',
            'Data_Lamp_Dark',
            'Data_Lamp_Ratio',
            'Data_Norm_PMT',
            'Data_Photo_Absolute',
            'Data_PMT',
            'Data_PMT_Dark',
            'Data_PMT_Signal',
            'Data_PMT_Temp',
            'Data_Sox_Pressure',
            'Data_RCell_Temp',
            'Data_Ref_4096mV',
            'Data_Ref_Ground',
            'Data_REF_V_4096_Dark',
            'Data_REF_V_4096_Light',
            'Data_Sample_Flow',
            'Data_SO2_Concentration',
            'Data_Stability',
            'Data_UV_Lamp',            

            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_WindDir',
            'Data_WindSpeed',	
            'Data_Pressure',
            'Data_DryA',
            'Data_GrassA',
            'Data_HumA',

            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class NOX_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = NOX_Data
        fields = [
            'id', 
            'Node_ID',
            'Data_DateTime',
            'Data_Box_Temp',
            'Data_HVPS',
            'Data_NO_Conc',
            'Data_NO_Norm_Offset',
            'Data_NO_Slope',
            'Data_NO_Stability',
            'Data_NO2_Conc',
            'Data_NO2_Stability',
            'Data_Norm_PMT',
            'Data_NOX_Conc',
            'Data_NOx_Norm_Offset',
            'Data_NOx_Slope',
            'Data_NOX_Stability',
            'Data_PMT_Signal',
            'Data_PMT_Temp',
            'Data_Ref_4096mV',
            'Data_Ref_Ground',
            'Data_Rx_Cell_Press',
            'Data_Rx_Cell_Temp',
            'Data_Sample_Flow',        

            'Data_MaxGust',
            'Data_MaxGustDir',
            'Data_WindDir',
            'Data_WindSpeed',	
            'Data_Pressure',
            'Data_DryA',
            'Data_GrassA',
            'Data_HumA',

            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status',
        ]

class Nodes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Nodes
        fields = [
            'id',
            'Node_Name',
            'Node_Description',
            'Node_Ip',
            'Node_Device_ID',
            'Asset_Ip',
            'Node_ID',
            'Node_Lat',
            'Node_Lng',
            'Node_X',
            'Node_Y',
            'Node_Z',
            'Status',
            'Asset_Status',
            'Asset_Status_Description',
            'Node_Status',
            'Node_Status_Description',
            'Server_Status',
            'Server_Status_Description',
            'Type',
            'Location',
            'Client',
            'Category',
        ]

class Node_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Type
        fields = [
            'id',
            'Type_Name',
            'Type_Description',
            'Type_Make',
            'Type_Model',
            'Type_Kwargs',
            'Type_Args',
        ]

class Node_Location_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Location
        fields = [
            'id',
            'Location_Name',
            'Location_Description',
            'Location_Lat',
            'Location_Lng',
            'Site',
        ]

class Clients_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            'id',
            'Client_Name',
            'Client_Description',
        ]

class Node_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Category
        fields = [
            'id',
            'Category_Name',
            'Category_Description',
            'Client',
        ]

class Autosonde_Soundings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Autosonde_Soundings
        fields = [
            'id',
            'Node_ID',
            'Data_Day',
            'Data_Type',
            'Data_Stage_1',
            'Data_Stage_2',
            'Data_Stage_3',
            'Data_Stage_4',
            'Data_Stage_5',
            'Data_Stage_6',
            'Data_Stage_7',
        ]

class Autosonde_Sounding_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Autosonde_Sounding_Data
        fields = [
            'id',
            'Sounding_ID',
            'Data_DateTime',
            'Data_EVSS',
            'Data_Pressure',
            'Data_Geopotential_Height',
            'Data_Lat',
            'Data_Lng',
            'Data_Air_Temperature',
            'Data_Dewpoint_Temperature',
            'Data_Direction',
            'Data_Speed',
        ]

class Autosonde_Logs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Autosonde_Logs
        fields = [
            'id',
            'Node_ID',
            'Log_DateTime',
            'Log_Type',
            'Log_Details',
        ]

class Autosonde_Ground_Station_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Autosonde_Ground_Station
        fields = [
            'id',
            'Node_ID',
            'Data_DateTime',
            'Met_Gust_Max',
            'Met_Gust_Direction',
            'Met_Wind_Direction',
            'Met_Wind_Speed',
            'Met_Pressure',
            'Met_Temperature_Dry',
            'Met_Temperature_Grass',
            'Met_Humidity',
            'Station_Supply_Voltage',
            'Station_Supply_L1',
            'Station_Supply_L2',
            'Station_Supply_L3',
            'Station_UPS_Battery_Level',
            'Station_UPS_Battery_Voltage',
            'Station_UPS_Est_Run_Time',
            'Station_UPS_Frequency',
            'Station_UPS_Load',
            'Station_UPS_Status',
            'Station_UPS_Output_Voltage',
            'Station_UPS_Temperature',
        ]

class UPS_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UPS
        fields = [
            'id',
            'Node_ID',
            'Log_DateTime',
            'Supply_Voltage',
            'Supply_L1',
            'Supply_L2',
            'Supply_L3',
            'UPS_Battery_Level',
            'UPS_Battery_Voltage',
            'UPS_Est_Run_Time',
            'UPS_Frequency',
            'UPS_Load',
            'UPS_Status',
            'UPS_Output_Voltage',
            'UPS_Temperature',
        ]       

class Generator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Generator
        fields = [
            'id',
            'Node_ID',
            'Log_DateTime',
            'Generator_Voltage',
            'Generator_L1',
            'Generator_L2',
            'Generator_L3',
            'Generator_Battery_Level',
            'Generator_Battery_Voltage',
            'Generator_Frequency',
            'Generator_Load',
            'Generator_Status',
            'Generator_Output_Voltage',
            'Generator_Oil_Temperature',
            'Generator_Coolent_Temperature',
            'Generator_Oil_Pressure',
            'Generator_Fuel_Level',
            'Generator_Running_Hours',
        ]           