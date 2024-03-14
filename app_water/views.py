from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
import pandas as pd
import numpy as np
#import tensorflow as tf

from datetime import timedelta, datetime, date

from pandas import to_datetime

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Meter_List,
    Water_Meter,
    Meter_Readings,
    Meter_Readings_Ave_WDH,
)

from .serializers import (
    Meter_List_Serializer,
    Readings_Serializer,
    Meter_Readings_Serializer,
    Meter_Readings_Ave_WDH_Serializer,
)

from django.utils import timezone

#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
#from reportlab.lib.styles import getSampleStyleSheet
import os

#def generate_pdf_save():
#    # Create the directory if it doesn't exist
#    directory = 'app_water/static/app_water/reports'
#    if not os.path.exists(directory):
#        os.makedirs(directory)

#    # Create a new PDF document
#    doc = SimpleDocTemplate(os.path.join(directory, "hello_world.pdf"), pagesize=letter)

#    # Create a list to hold the PDF elements
#    elements = []

#    # Add the text "Hello World"
#    styles = getSampleStyleSheet()
#    text = Paragraph("Hello World", styles["BodyText"])
#    elements.append(text)

#    # Build the PDF
#    doc.build(elements)


########################################################################################
################################### GET REPORTS API ###################################
class Reports_ViewSet(viewsets.ModelViewSet):
    def list(self, request):
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        resolution = self.request.query_params.get('resolution')
        organization = self.request.query_params.get('org')

        print(organization)

        #generate_pdf_save()

        reports = {}
        try:
            reports['Data'] = json.loads(Meter_List.objects.filter(Status = 0, Organization = organization).order_by('Category').to_dataframe().to_json(orient="table"))['data']
            for meter in reports['Data']:
                meter.update(get_meter_readings_by_id_resolution_date(meter['id'], resolution, start_datetime, end_datetime))
        except Exception as e:
            print('{!r}; Get Meters failed - '.format(e))
            Response({})
        return Response(json.dumps(reports))
################################### GET REPORTS API ###################################
########################################################################################

########################################################################################
################################### GET ANALYSIS API ###################################
class Analysis_ViewSet(viewsets.ModelViewSet):
    def list(self, request):
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        resolution = self.request.query_params.get('resolution')

        analysis_data = {}
        try:
            df = pd.DataFrame(Water_Meter.objects.filter(Data_DateTime__gte = start_datetime, Data_DateTime__lte = end_datetime, Meter__Status = 0).values('id', 'Meter__Name', 'Data_DateTime', 'Pulses', 'Meter', 'Meter__Pulse_Unit_Value').order_by('-id'))
            df["Water"] = df["Pulses"] * df["Meter__Pulse_Unit_Value"]
            df = df.pivot_table(values='Water', index='Data_DateTime', columns='Meter__Name', aggfunc='first').sort_index(ascending=True).resample(resolution).sum().fillna(method='backfill')
            analysis_data = json.loads(df.to_json(orient="table"))['data']
        except Exception as e:
            print('{!r}; Get data analysis data failed - '.format(e))
            Response({})
        return Response(json.dumps(analysis_data))
################################### GET ANALYSIS API ###################################
########################################################################################

########################################################################################
################################### GET Readings API ###################################
class GetWaterDataByIdAndDates_ViewSet(viewsets.ModelViewSet):
    def list(self, request):
        meter_id = self.request.query_params.get('meter_id')
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        resolution = self.request.query_params.get('resolution')

        print(meter_id)
        print(start_datetime)
        print(end_datetime)
        print(resolution)

        meters = {}
        try:
            meters['Data'] = json.loads(Meter_List.objects.filter(id = meter_id, Status = 0).order_by('Category').to_dataframe().to_json(orient="table"))['data']
            for meter in meters['Data']:
                meter.update(get_meter_readings_by_id_resolution_date(meter['id'], resolution, start_datetime, end_datetime))
                meter.update(get_average_readings_by_id(meter['id']))
        except Exception as e:
            print('{!r}; Get Meters failed - '.format(e))
            Response({})
        return Response(json.dumps(meters))

def get_meter_readings_by_id_resolution_date(meter_id, resolution, start_datetime, end_datetime):    
    try:
        readings = {'readings': json.loads(Water_Meter.objects.filter(Meter = meter_id, Data_DateTime__gte = start_datetime, Data_DateTime__lte = end_datetime).order_by('-id').to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample(resolution).sum().fillna(method='backfill').to_json(orient="table"))['data']}
        #print(readings)
    except Exception as e:
        print('{!r}; Get Readings failed - '.format(e))
        return {'readings': []}
    return readings

def get_average_readings_by_id(meter_id):    
    try:
        # Print a header indicating which meter is being processed
        print('####### ' + str(meter_id) + ' #########')
        one_month_ago = timezone.now() - timedelta(days=30)
        # Get the latest record for the meter
        latest_record = Meter_Readings_Ave_WDH.objects.filter(Meter_Id=Meter_List.objects.get(id=meter_id)).order_by('-Last_Updated').first()
        print(latest_record)
        # Check if the latest record is older than a month
        if latest_record is None or latest_record.Last_Updated <= one_month_ago:
            # Load and preprocess data from Water_Meter model
            df = pd.DataFrame(Water_Meter.objects.all().values('Data_DateTime', 'Pulses').filter(Meter=meter_id).order_by('-id')[:6000])
            df_new = df.set_index('Data_DateTime')
            data = []  # List to store daily average water usage data
            day_array = []  # List to store hourly average water usage data for each day
            # Loop through each day of the week and hour of the day
            for day in range(7):
                for hour in range(24):
                    # Filter the DataFrame to include only rows with the specified hour and day of the week
                    filtered_df = df_new[(df_new.index.hour == hour) & (df_new.index.dayofweek == day)]

                    mean_value = round(filtered_df['Pulses'].mean()*4, 3)
                    min_value = round(filtered_df['Pulses'].min(), 3)
                    max_value = round(filtered_df['Pulses'].max(), 3)

                    mean_value = 0.0 if np.isnan(mean_value) else mean_value
                    min_value = 0.0 if np.isnan(min_value) else min_value
                    max_value = 0.0 if np.isnan(max_value) else max_value

                    day_array.append([mean_value, min_value, max_value])

                    #day_array.append([round(filtered_df['Pulses'].mean()*4, 3), round(filtered_df['Pulses'].min(), 3), round(filtered_df['Pulses'].max(), 3)])
                data.append(day_array)  # Add the last day's data to daily data
                day_array = []

            #print(df_new[(df_new.index.hour == 16) & (df_new.index.dayofweek == 1)])

            # Store daily average water usage data in Meter_Readings_Ave_WDH model
            Meter_Readings_Ave_WDH.objects.update_or_create(
                Meter_Id = Meter_List.objects.get(id=meter_id),
                defaults={
                    'Last_Updated': datetime.now(),
                    'Day_0': str(data[0]), 
                    'Day_1': str(data[1]), 
                    'Day_2': str(data[2]), 
                    'Day_3': str(data[3]), 
                    'Day_4': str(data[4]), 
                    'Day_5': str(data[5]), 
                    'Day_6': str(data[6]),
                }
            )
            # Retrieve the latest baseline data for the meter and return as a dictionary object
            baseline = {'baseline': json.loads(Meter_Readings_Ave_WDH.objects.filter(Meter_Id=Meter_List.objects.get(id=meter_id)).to_dataframe(index='Last_Updated').to_json(orient="table"))['data'][0]}
        else:
            baseline = {'baseline': json.loads(Meter_Readings_Ave_WDH.objects.filter(Meter_Id=Meter_List.objects.get(id=meter_id)).to_dataframe(index='Last_Updated').to_json(orient="table"))['data'][0]}
       
    except Exception as e:
        print('{!r}; Get baseline failed - '.format(e))
        return {'baseline': []}
    return baseline
################################### GET Readings API ###################################
########################################################################################

class Meter_Readings_Ave_WDH_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings_Ave_WDH.objects.all().order_by('Last_Updated')
    serializer_class = Meter_Readings_Ave_WDH_Serializer

class Pulses_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings.objects.all().order_by('Data_DateTime')
    serializer_class = Meter_Readings_Serializer

    def create(self, request):
        print(self.request.data)

        data = request.data      
        pulse_count = data['Pulse_Count'] 
        
        print(pulse_count)
        print(type(pulse_count))
                   
        msg_water_meter = Water_Meter.objects.create(
            Meter = Meter_List.objects.get(id = data['Meter_Id']),
            Data_DateTime = data['Data_DateTime'],
            Pulses = int(pulse_count), 
            Battery_Level = 100,
            Battery_Voltage = 3.3,
        )
        
        return Response(data = "done")

################################################################################################
################################### PUT LoraWAN Readings API ###################################
class Meter_Readings_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings.objects.all().order_by('Data_DateTime')
    serializer_class = Meter_Readings_Serializer

    def create(self, request):
        # Data Format: {'uplink_message': {'decoded_payload': {'Data_DateTime': '2022-09-13T13:18:25.903Z', 'Meter_Id': 1, 'Pulse_Count': 407, 'Pulses': 0}}}        
        data = request.data['uplink_message']['decoded_payload']
        print(self.request.data)
        pulse_count = 0
        this_pulse_count = data['Pulse_Count']

        if Meter_Readings.objects.filter(Meter_Id = data['Meter_Id']).exists():
            last_pulse_count = Meter_Readings.objects.filter(Meter_Id = data['Meter_Id']).latest('id').Pulse_Count
        else:
            last_pulse_count = 0

        if this_pulse_count < last_pulse_count:
            pulse_count = this_pulse_count
        else:
            pulse_count = this_pulse_count - last_pulse_count

        #pulse_count = this_pulse_count - last_pulse_count

        print(this_pulse_count)
        print(last_pulse_count)
        print(pulse_count)
        
        if (pulse_count >= 0):
            msg_meter_readings = Meter_Readings.objects.create(
                Meter_Id = Meter_List.objects.get(id = data['Meter_Id']),
                Data_DateTime = data['Data_DateTime'], 
                Pulse_Count = data['Pulse_Count'], 
                Pulses = pulse_count
            )
            msg_water_meter = Water_Meter.objects.create(
                Meter = Meter_List.objects.get(id = data['Meter_Id']),
                Data_DateTime = data['Data_DateTime'],
                Pulses = pulse_count, 
                Battery_Level = 100,
                Battery_Voltage = 3.3,
            )
        
        return Response(data = "done")
################################### PUT LoraWAN Readings API ###################################
################################################################################################
        
class Readings_ViewSet(viewsets.ModelViewSet):
    queryset = Water_Meter.objects.all().order_by('Data_DateTime')
    serializer_class = Readings_Serializer
    
class Meter_List_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_List.objects.filter(Status = 0)
    serializer_class = Meter_List_Serializer

    def list(self, request):
        data = json.loads(get_meters())
        return Response(data)

    def create(self, request):
        print(request.data)

@login_required(login_url="/login/")
def index(request):
    context = {}
    context['meter_list_data'] = get_meters(request.user.profile.organization)
    context['meter_list'] = Meter_List.objects.filter(Status = 0, Organization = request.user.profile.organization)
    
    html_template = loader.get_template( 'app_water/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        context['test'] = 'this is a testicle...'

        html_template = loader.get_template('app_water/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

def get_meters(Organization):
    meters = {}
    try:
        meters['Data'] = json.loads(Meter_List.objects.filter(Status = 0, Organization = Organization).order_by('Category').to_dataframe().to_json(orient="table"))['data']
    except Exception as e:
        print('{!r}; Get Meters failed - '.format(e))
    return json.dumps(meters)




#def predict(meter_id):   
#    
#    # Load and preprocess data from Water_Meter model
#    df = pd.DataFrame(Water_Meter.objects.all().values('Data_DateTime', 'Pulses', 'Meter__Pulse_Unit_Value').filter(Meter=meter_id).order_by('-id'))
#    df_new = df.set_index('Data_DateTime')
#    
#    # Define features (hour of day, day of week) and labels (water consumption in pulses)
#    features = ['hour_of_day', 'day_of_week']
#    labels = ['pulses']
#    
#    # Create a new DataFrame with the features and labels
#    df_features = pd.DataFrame(columns=features)
#    df_labels = pd.DataFrame(columns=labels)
#    
#    # Loop through each day of the week and hour of the day
#    for day in range(7):
#        for hour in range(24):
#            # Filter the DataFrame to include only rows with the specified hour and day of the week
#            filtered_df = df_new[(df_new.index.hour == hour) & (df_new.index.dayofweek == day)]
#    
#            # Calculate the mean and total water consumption for the current hour and day
#            mean_water_consumption = filtered_df['Pulses'].mean()
#            total_water_consumption = filtered_df['Pulses'].sum()
#    
#            # Add the features and labels for the current hour and day to the new DataFrames
#            df_features = df_features.append(pd.DataFrame([[hour, day]], columns=features), ignore_index=True)
#            df_labels = df_labels.append(pd.DataFrame([[total_water_consumption]], columns=labels), ignore_index=True)
#    
#    # Convert the DataFrames to NumPy arrays
#    X = df_features.values.astype(np.float32)
#    y = df_labels.values.astype(np.float32)
#    
#    # Split the data into training and testing sets
#    train_size = int(0.8 * len(X))
#    X_train, X_test = X[:train_size], X[train_size:]
#    y_train, y_test = y[:train_size], y[train_size:]
#    
#    # Define the TensorFlow model
#    model = tf.keras.Sequential([
#        tf.keras.layers.Dense(64, activation='relu', input_dim=2),
#        tf.keras.layers.Dense(1)
#    ])
#    
#    # Compile the model
#    model.compile(optimizer='adam', loss='mse')
#    
#    # Train the model
#    model.fit(X_train, y_train, epochs=100)
#    
#    # Evaluate the model on the testing set
#    loss = model.evaluate(X_test, y_test)
#    print(f"Test loss: {loss}")
#    
#    # Use the model to make predictions for a given day and hour
#    day = 2  # Wednesday
#    hour = 5  # Noon
#    features_for_prediction = np.array([[hour, day]])
#    predicted_water_consumption = model.predict(features_for_prediction)[0][0]
#    #print(f"Predicted water consumption at {hour}:00 on Wednesday: {predicted_water_consumption} pulses")
#
#    data = []  # List to store daily average water usage data
#    day_array = []  # List to store hourly average water usage data for each day
#    # Loop through each day of the week and hour of the day
#    for day in range(7):
#        for hour in range(24):
#            # Filter the DataFrame to include only rows with the specified hour and day of the week
#            features_for_prediction = np.array([[hour, day]])
#            predicted_water_consumption = model.predict(features_for_prediction)[0][0]
#            day_array.append([round(predicted_water_consumption, 3)])
#        data.append(day_array)  # Add the last day's data to daily data
#        day_array = []
#    print(data)
