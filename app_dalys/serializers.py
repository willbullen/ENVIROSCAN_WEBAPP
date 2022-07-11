from rest_framework import serializers
from .models import Node_List, Node_Water, Node_Power

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

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'