from rest_framework import serializers
from .models import ComponentChangeLog, RationTableLog, RationTableComponentLog

# Serializer for ComponentChangeLog
class ComponentChangeLogSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name', read_only=True)

    class Meta:
        model = ComponentChangeLog
        fields = ['id', 'component', 'component_name', 'field_name', 'old_value', 'new_value', 'changed_at']

# Serializer for RationTableLog
class RationTableLogSerializer(serializers.ModelSerializer):
    ration_table_name = serializers.CharField(source='ration_table.name', read_only=True)

    class Meta:
        model = RationTableLog
        fields = ['id', 'ration_table', 'ration_table_name', 'action', 'description', 'changed_at']

# Serializer for RationTableComponentLog
class RationTableComponentLogSerializer(serializers.ModelSerializer):
    table_component_name = serializers.CharField(source='table_component.component.name', read_only=True)
    ration_table_name = serializers.CharField(source='table_component.ration_table.name', read_only=True)

    class Meta:
        model = RationTableComponentLog
        fields = ['id', 'table_component', 'table_component_name', 'ration_table_name', 'action', 'old_quantity', 'new_quantity', 'changed_at']
