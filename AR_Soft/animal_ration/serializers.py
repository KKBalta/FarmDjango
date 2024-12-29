# animal_ration/serializers.py
from rest_framework import serializers
from .models import AnimalRationLog
from Animal.models import Animal
from ration_components.models import RationTable

class AnimalRationLogSerializer(serializers.ModelSerializer):
    animal_eartag = serializers.CharField(source="animal.eartag", read_only=True)
    ration_table_name = serializers.CharField(source="ration_table.name", read_only=True)

    class Meta:
        model = AnimalRationLog
        fields = ['id', 'animal', 'animal_eartag', 'ration_table', 'ration_table_name', 'start_date', 'end_date', 'is_active']

    def create(self, validated_data):
        """
        Simply call the model's save method.
        """
        return AnimalRationLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Allow updating the instance and handle transitions.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance