# serializers.py
from rest_framework import serializers
from .models import Slaughter
from datetime import datetime, date

class SlaughterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slaughter
        fields = ['id', 'animal', 'date', 'carcas_weight', 'sale_price', 'kdv']
    
    # Validation for carcass weight
    def validate_carcas_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Carcass weight must be a positive number.")
        return value

    # Validation for sale price
    def validate_sale_price(self, value):
        if value is None:
            raise serializers.ValidationError("Sale price cannot be null.")
        if value <= 0:
            raise serializers.ValidationError("Sale price must be a positive number.")
        return value

    # Default KDV value
    def create(self, validated_data):
        validated_data.setdefault('kdv', 0.0)  # Default KDV to 0.0 if not provided
        return super().create(validated_data)