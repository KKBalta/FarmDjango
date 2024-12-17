# Slaughter/serializers.py
from rest_framework import serializers
from .models import Slaughter

class SlaughterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slaughter
        fields = ['id', 'animal', 'date', 'carcas_weight', 'sale_price', 'kdv']
