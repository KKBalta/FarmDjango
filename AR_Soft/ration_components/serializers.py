from rest_framework import serializers
from .models import RationComponent, RationTable, RationTableComponent, RationComponentChange
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


# Serializer for RationComponentChange
class RationComponentChangeSerializer(serializers.ModelSerializer):
    ration_table_component_id = serializers.IntegerField()
    ration_table_name = serializers.CharField()
    component_name = serializers.CharField()
    action = serializers.ChoiceField(choices=RationComponentChange.ACTION_CHOICES)
    old_quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    new_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True, default=0.0)
    old_price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    new_price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    old_dry_matter = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    new_dry_matter = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    old_calori = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    new_calori = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    old_nisasta = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    new_nisasta = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    changed_at = serializers.DateTimeField()

    class Meta:
        model = RationComponentChange
        fields = [
            'id',
            'ration_table_component_id',
            'ration_table_name',
            'component_name',
            'action',
            'old_quantity',
            'new_quantity',
            'old_price',
            'new_price',
            'old_dry_matter',
            'new_dry_matter',
            'old_calori',
            'new_calori',
            'old_nisasta',
            'new_nisasta',
            'changed_at',
        ]
