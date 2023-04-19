# -*- encoding: utf-8 -*-
from django import forms
from .models import Reports_Project

class ProjectCreateForm(forms.ModelForm):
    Project_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Project Name",                
                "class": "form-control"
            }
        ))
    Project_Description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Project Description",                
                "class": "form-control"
            }
        ))
    Project_Status = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder" : "1",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = Reports_Project
        fields = ['Project_Name', 'Project_Description', 'Project_Status']