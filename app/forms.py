from django import forms
from django.contrib.auth.models import User

from data.models import CMMS_Jobs, CMMS_Job_Tasks

class CMMS_Jobs_Form(forms.ModelForm):
    class Meta:
        model = CMMS_Jobs
        fields = [
            'Node_ID', 
            'Job_Created_DateTime', 
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
            'Job_Completed_Comments'
        ]

class CMMS_Job_Tasks_Form(forms.ModelForm):
    class Meta:
        model = CMMS_Job_Tasks
        fields = [
            'Job', 
            'Job_Task_Title', 
            'Job_Task_Description', 
            'Job_Task_Completed_Date', 
            'Job_Task_Completed_Comments'
        ]