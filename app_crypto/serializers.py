from rest_framework import serializers
from .models import Kraken_Data

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
