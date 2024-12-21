from rest_framework import serializers
from .models import RationComponent, RationTable, RationTableComponent, RationComponentChange
from rest_framework.exceptions import ValidationError

# Serializer for RationComponent
class RationComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationComponent
        fields = ['id', 'name', 'description']

class RationTableComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationTableComponent
        fields = ['id', 'ration_table', 'component', 'quantity']

# Serializer for RationTable
class RationTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationTable
        fields = ['id', 'name', 'description']

# Serializer for RationComponentChange
class RationComponentChangeSerializer(serializers.ModelSerializer):
    ration_table_component = RationTableComponentSerializer()

    class Meta:
        model = RationComponentChange
        fields = ['id', 'ration_table_component', 'old_quantity', 'new_quantity', 'changed_at']
