from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.forms.widgets import NumberInput, DateInput

from data.models import Nodes, CMMS_Jobs, CMMS_Job_Tasks, CMMS_Job_Status, CMMS_Job_Types, CMMS_Job_Priority, CMMS_Job_Schedule_Type, CMMS_Job_Schedule_Period

class CMMS_Jobs_Form(forms.ModelForm):

    Node_ID = forms.ModelChoiceField(queryset = Nodes.objects.all(), widget = forms.Select(attrs = {'class': 'form-select'}),)
    #Author = forms.CharField(widget = forms.HiddenInput())
    Job_Title = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title here.'}),)
    Job_Description = forms.CharField(required = False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),)
    Job_Status = forms.ModelChoiceField(required = False, queryset = CMMS_Job_Status.objects.all(), widget = forms.Select(attrs = {'class': 'form-select'}),)
    Job_Start_Date = forms.DateField(required = False, widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter a start date: '}),)
    Job_End_Date = forms.DateField(required = False, widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter a end date: '}),)
    Job_Type = forms.ModelChoiceField(required = False, queryset = CMMS_Job_Types.objects.all(), widget = forms.Select(attrs = {'class': 'form-select'}),)
    Job_Priority = forms.ModelChoiceField(required = False, queryset = CMMS_Job_Priority.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}),)
    Job_Schedule_Type = forms.ModelChoiceField(required = False, queryset = CMMS_Job_Schedule_Type.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}),)
    Job_Schedule_Period = forms.ModelChoiceField(required = False, queryset = CMMS_Job_Schedule_Period.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}),)    
    Job_Schedule_Period_Value = forms.CharField(required = False, widget=forms.TextInput(attrs={'class': 'form-control'}),)
    Job_Completed_Date = forms.DateField(required = False, widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter a date: '}),)
    Job_Completed_Comments = forms.CharField(required = False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),)

    class Meta:
        model = CMMS_Jobs
        fields = [
            'Node_ID',
            #'Author',
            'Job_Title', 
            'Job_Description', 
            'Job_Start_Date', 
            'Job_End_Date', 
            'Job_Type', 
            'Job_Status', 
            'Job_Priority', 
            'Job_Schedule_Type', 
            'Job_Schedule_Period', 
            'Job_Schedule_Period_Value', 
            'Job_Completed_Date',
            'Job_Completed_Comments'
        ]

class CMMS_Job_Tasks_Form(forms.ModelForm):

    Job_Task_Title = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title here.'}),)
    Job_Task_Description = forms.CharField(required = False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),)
    Job_Task_Status = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-check-input', 'onchange': 'showHide(this.id)'}),)
    Job_Task_Completed_Comments = forms.CharField(required = False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),)

    class Meta:
        model = CMMS_Job_Tasks
        fields = [
            'Job',
            'Job_Task_Title',
            'Job_Task_Description',
            'Job_Task_Status',
            'Job_Task_Completed_Comments'
        ]

TasksFormSet = forms.inlineformset_factory(
    CMMS_Jobs, 
    CMMS_Job_Tasks, 
    form=CMMS_Job_Tasks_Form,
    extra = 1,
)