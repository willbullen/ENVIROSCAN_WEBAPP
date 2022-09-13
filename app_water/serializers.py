from rest_framework import serializers
from .models import Meter_List, Water_Meter, Meter_Readings

class Meter_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Meter_List
        fields = '__all__'

class Readings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Water_Meter
        fields = '__all__'

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

class Meter_Readings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Meter_Readings
        fields = '__all__'