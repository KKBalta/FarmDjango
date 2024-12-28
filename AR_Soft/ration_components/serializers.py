from rest_framework import serializers
from .models import RationComponent, RationTable, RationTableComponent
from rest_framework.exceptions import ValidationError
from django.utils import timezone


# Serializer for RationComponent
class RationComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationComponent
        fields = ['id', 'name', 'description', 'dry_matter', 'calori', 'nisasta', 'price']


# Serializer for RationTableComponent
class RationTableComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationTableComponent
        fields = ['id', 'ration_table', 'component', 'quantity']


# Serializer for RationTable
class RationTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationTable
        fields = ['id', 'name', 'description']