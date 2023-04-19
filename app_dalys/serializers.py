from rest_framework import serializers
from .models import Node_List, Node_Water, Node_Power, Node_Temperature, Reports_Project, Reports_Levels, Reports_Models, Reports_Scans

class Node_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_List
        fields = '__all__'

class Water_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Water
        fields = '__all__'

class Power_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Power
        fields = '__all__'

class Temperature_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Node_Temperature
        fields = '__all__'

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

###########
# 3D REPORTS
class Reports_Project_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reports_Project
        fields = '__all__'

class Reports_Levels_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reports_Levels
        fields = '__all__'

class Reports_Models_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reports_Models
        fields = '__all__'

class Reports_Scans_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Reports_Scans
        fields = '__all__'