# animal_ration/serializers.py
from rest_framework import serializers
from .models import AnimalRationLog
from Animal.models import Animal
from ration_components.models import RationTable

class AnimalRationLogSerializer(serializers.ModelSerializer):
    animal_eartag = serializers.CharField(source="animal.eartag", read_only=True)
    ration_table_name = serializers.CharField(source="ration_table.name", read_only=True)
    start_date = serializers.DateTimeField(read_only=True)  # Automatically set
    end_date = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = AnimalRationLog
        fields = ['id', 'animal', 'animal_eartag', 'ration_table', 'ration_table_name', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['animal_eartag', 'ration_table_name', 'start_date']

    def validate(self, data):
        """
        Ensure that only one active ration is allowed per animal.
        """
        animal = data.get('animal')
        is_active = data.get('is_active', True)

        if is_active and AnimalRationLog.objects.filter(animal=animal, is_active=True).exists():
            raise serializers.ValidationError(
                f"Animal '{animal.eartag}' already has an active ration."
            )

        return data

    def create(self, validated_data):
        """
        Automatically deactivate existing active logs when a new log is created as active.
        """
        animal = validated_data['animal']
        is_active = validated_data.get('is_active', True)

        if is_active:
            # Deactivate existing active logs for this animal
            AnimalRationLog.objects.filter(animal=animal, is_active=True).update(is_active=False, end_date=validated_data['start_date'])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Handle updates while maintaining the integrity of active logs.
        """
        is_active = validated_data.get('is_active', instance.is_active)

        if is_active and not instance.is_active:
            # If the log is being activated, deactivate others for the same animal
            AnimalRationLog.objects.filter(animal=instance.animal, is_active=True).update(is_active=False, end_date=validated_data.get('start_date', instance.start_date))

        return super().update(instance, validated_data)
