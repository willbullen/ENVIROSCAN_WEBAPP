from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
from django.contrib import messages

from data.models import (
    CMMS_Jobs, 
    CMMS_Job_Tasks, 
    UPS, 
    Generator, 
    Autosonde_Ground_Station, 
    Aethalometer_Data, 
    Autosonde_Soundings, 
    Autosonde_Sounding_Data, 
    Autosonde_Logs, 
    Nodes, 
    SOX_Data, 
    NOX_Data, 
    Picarro_Data, 
    Tucson_Data,
    DAQC_Fields
)

from django.core import serializers

from .forms import CMMS_Jobs_Form, CMMS_Job_Tasks_Form, TasksFormSet
from django.core import serializers

@login_required(login_url="/login/")
def index(request):
    
    context = {
        'asset_list': Nodes.objects.all(),
        'segment': 'index',
    }

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def cmms(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            Job_ID = request.GET['id']
    context = {
        'open_jobs': get_jobs(2),
        'in_progress_jobs': get_jobs(1),
        'closed_jobs': get_jobs(3),
    }
    html_template = loader.get_template('dashboard_cmms.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def cmms_edit(request, pk):
    job = get_object_or_404(CMMS_Jobs, pk=pk)
    if request.method == "POST":
        job_form = CMMS_Jobs_Form(request.POST, instance=job)
        if job_form.is_valid():
            job_task = job_form.save()
            tasks_formset = TasksFormSet(request.POST, instance=job_task)
            print(tasks_formset.errors)
            if tasks_formset.is_valid():
                tasks_formset.save()
                return HttpResponse('../')
            else:
                print('SHIT TASK FORM')
        else:
            print('SHIT JOB FORM')        
    else:
        job_form = CMMS_Jobs_Form(instance=job)
        tasks_formset = TasksFormSet(instance=job)
    context = {
        'job_form': job_form,
        'tasks_formset': tasks_formset,
        'open_jobs': get_jobs(2),
        'in_progress_jobs': get_jobs(1),
        'closed_jobs': get_jobs(3),
    }
    html_template = loader.get_template('dashboard_cmms_edit.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def cmms_add(request):
    context = {}
    if request.method == "POST":
        job_form = CMMS_Jobs_Form(request.POST)
        if job_form.is_valid():
            job = job_form.save()
            tasks_formset = TasksFormSet(request.POST, instance=job)
            print(tasks_formset.errors)
            if tasks_formset.is_valid():
                tasks_formset.save()
                return HttpResponse('../')
    else:
        job_form = CMMS_Jobs_Form()
        tasks_formset = TasksFormSet()
    context = {
        'job_form': job_form,
        'tasks_formset': tasks_formset,
        'open_jobs': get_jobs(2),
        'in_progress_jobs': get_jobs(1),
        'closed_jobs': get_jobs(3),
    }
    html_template = loader.get_template('dashboard_cmms_add.html')
    return HttpResponse(html_template.render(context, request))

#-- daqc
@login_required(login_url="/login/")
def daqc(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_test_data(Node_ID, SOX_Data)
    context['Asset_List'] = Nodes.objects.all() 

    html_template = loader.get_template('dashboard_daqc.html')
    return HttpResponse(html_template.render(context, request))   

#-- sox
@login_required(login_url="/login/")
def sox(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, SOX_Data)           
    context['Current_Data'] = get_current_data(Node_ID, SOX_Data)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_sox.html')
    return HttpResponse(html_template.render(context, request))        
    
#-- nox
@login_required(login_url="/login/")
def nox(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, NOX_Data)           
    context['Current_Data'] = get_current_data(Node_ID, NOX_Data)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_nox.html')
    return HttpResponse(html_template.render(context, request)) 

#-- picarro
@login_required(login_url="/login/")
def picarro(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, Picarro_Data)           
    context['Current_Data'] = get_current_data(Node_ID, Picarro_Data)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_picarro.html')
    return HttpResponse(html_template.render(context, request)) 

#-- aethalometer
@login_required(login_url="/login/")
def aethalometer(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, Aethalometer_Data)           
    context['Current_Data'] = get_current_data(Node_ID, Aethalometer_Data)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_aethalometer.html')
    return HttpResponse(html_template.render(context, request)) 

#-- autosonde
@login_required(login_url="/login/")
def autosonde(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    Sounding_ID = Autosonde_Soundings.objects.filter(Node_ID = Node_ID).latest('id').id                   
    context['Ground_Station_Data'] = get_groundstation_data(Node_ID, Autosonde_Ground_Station) # GROUND STATION DATA            
    context['Sounding_Data'] = get_sounding_data(Node_ID, Sounding_ID, Autosonde_Sounding_Data) # SOUNDING            
    context['Soundings_Data'] = get_soundings(Node_ID, Sounding_ID, Autosonde_Soundings) # SOUNDING DATA            
    context['Log_Data'] = get_log_data(Node_ID, Autosonde_Logs) # LOG DATA            
    context['Status_Data'] = get_status_data() # STATUS DATA            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA

    html_template = loader.get_template('dashboard_autosonde.html')
    return HttpResponse(html_template.render(context, request)) 

#-- tucson
@login_required(login_url="/login/")
def tucson(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, Tucson_Data)           
    context['Current_Data'] = get_current_data(Node_ID, Tucson_Data)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_tucson.html')
    return HttpResponse(html_template.render(context, request)) 

#-- generator
@login_required(login_url="/login/")
def generator(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, Generator)           
    context['Current_Data'] = get_current_data(Node_ID, Generator)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_generator.html')
    return HttpResponse(html_template.render(context, request)) 

#-- ups
@login_required(login_url="/login/")
def ups(request):
    context = {}

    if request.method == 'GET' and 'id' in request.GET:
        Node_ID = request.GET['id']
    else:
        Node_ID = '0'

    context['History_Data'] = get_history_data(Node_ID, UPS)           
    context['Current_Data'] = get_current_data(Node_ID, UPS)            
    context['Status_Data'] = get_status_data()            
    context['Setup_Data'] = get_setup_data(Node_ID, Nodes)

    html_template = loader.get_template('dashboard_ups.html')
    return HttpResponse(html_template.render(context, request)) 

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'page_404_error.html' )
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))   
        html_template = loader.get_template( 'page_404_error.html' )
        return HttpResponse(html_template.render(context, request))





def get_jobs(status):
    # -- JOBS
    jobs = []
    i = 0
    for job in CMMS_Jobs.objects.filter(Job_Status = status):
        tasks_total = CMMS_Job_Tasks.objects.filter(Job = job).count()
        task_completed = CMMS_Job_Tasks.objects.filter(Job = job, Job_Task_Status = True).count()
        task_completed_pecent = (tasks_total/task_completed)*100 if task_completed != 0 else 0
        task_completed_style = "style='width: 66%;'"
        jobs.append({
            "job_id": job.pk, 
            #"job_author": job.Author.username,
            "job_create_date": job.Job_Created_DateTime,
            "job_title": job.Job_Title, 
            "job_description": job.Job_Description,            
            "job_start_date": job.Job_Start_Date,
            "job_end_date": job.Job_End_Date,
            "job_type": job.Job_Type.Job_Type_Title,
            "job_status": job.Job_Status.Job_Status_Title,
            "job_priority": job.Job_Priority.Job_Priority_Title,
            "job_schedule_type": job.Job_Schedule_Type.Job_Schedule_Type_Title,
            "job_schedule_period": job.Job_Schedule_Period,
            "job_schedule_period_value": job.Job_Schedule_Period_Value,
            "job_completed_date": job.Job_Completed_Date,
            "job_completed_comments": job.Job_Completed_Comments,
            "tasks": [],
            "task_total": tasks_total,
            "task_completed": task_completed,
            "task_completed_pecent": task_completed_pecent,
            "task_completed_style": task_completed_style,
            "attachments": [],
        })
        tasks = CMMS_Job_Tasks.objects.filter(Job = job.id)
        for task in tasks:
            jobs[i]["tasks"].append({
                "task_id": task.pk, 
                "task_title": task.Job_Task_Title,
                "task_description": task.Job_Task_Description,
                "task_status": task.Job_Task_Status,
                "task_completed_date": task.Job_Task_Completed_Date,
                "task_completed_comments": task.Job_Task_Completed_Comments,
            })

        i += 1

    return jobs

def get_test_data(node_id, object):
    test = {}
    try:
        test['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:5000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').to_json(orient="table"))
        test['Data_Type'] = "HistoryData"
        test['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get History data failed - '.format(e))
    return json.dumps(test)

def get_setup_data(node_id, object):
    Setup = {}
    try:
        Setup['Data'] = json.loads(object.objects.filter(id = node_id).to_dataframe().to_json(orient="table"))
        Setup['Data_Type'] = "SetupData"
        Setup['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Setup data failed - '.format(e))
    return json.dumps(Setup)

def get_status_data():
    Status = {}
    try:
        Status['Data'] = json.loads(Nodes.objects.all().to_dataframe().to_json(orient="table"))
        Status['Data_Type'] = "StatusData"
        Status['Node_ID'] = 0
    except Exception as e:
        print('{!r}; Get Status data failed - '.format(e))
    return json.dumps(Status)

def get_current_data(node_id, object):
    Current = {}
    try:
        Current['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).last()]))[0]['fields']}
        Current['Data_Type'] = 'CurrentData'
        Current['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Current data failed - '.format(e))
    return json.dumps(Current)

def get_history_data(node_id, object):
    History = {}
    try:
        History['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
        History['Data_Type'] = "HistoryData"
        History['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get History data failed - '.format(e))
    return json.dumps(History)

def get_groundstation_data(node_id, object):
    Ground_Station = {}
    try:
        Ground_Station['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
        Ground_Station['Data_Type'] = "GroundstationData"
        Ground_Station['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Groundstation data failed - '.format(e))
    return json.dumps(Ground_Station)

def get_sounding_data(node_id, sounding_id, object):
    Sounding = {}
    try:
        Sounding['Data'] = json.loads(object.objects.filter(Sounding_ID = sounding_id).to_dataframe().to_json(orient="table"))
        Sounding['Data_Type'] = 'SoundingData'
        Sounding['Node_ID'] = node_id    
        Sounding['Sounding_ID'] = sounding_id
    except Exception as e:
        print('{!r}; Get Sounding data failed - '.format(e))
    return json.dumps(Sounding)

def get_soundings(node_id, sounding_id, object):
    Soundings = {}
    try:
        Soundings['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).latest('id')]))[0]['fields']}
        Soundings['Data_Type'] = 'SoundingsData'
        Soundings['Node_ID'] = node_id  
        Soundings['Sounding_ID'] = sounding_id
    except Exception as e:
        print('{!r}; Get Soundings data failed - '.format(e))
    return json.dumps(Soundings)

def get_log_data(node_id, object):
    Logs = {}
    try:
        Logs['Data'] = json.loads(object.objects.filter(Node_ID = node_id).to_dataframe().to_json(orient="table"))
        Logs['Data_Type'] = 'LogData'
        Logs['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Log data failed - '.format(e))
    return json.dumps(Logs)