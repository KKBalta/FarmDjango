# weight/serializers.py
from rest_framework import serializers
from .models import Weight
from django.utils import timezone

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['id', 'animal', 'weight', 'recorded_at']

    def validate(self, data):
        animal = data.get('animal')
        recorded_at = data.get('recorded_at')

        # Ensure recorded_at is set to the current time if not provided during creation
        if recorded_at is None and not self.instance:  # Only when creating a new object
            data['recorded_at'] = timezone.now()  # Set current date and time during creation

        # Check if the recorded date is in the future
        if recorded_at and recorded_at > timezone.now():
            raise serializers.ValidationError(
                {"recorded_at": "The recorded date cannot be in the future."}
            )

        # Validate that there are no duplicate records for the same animal and recorded_at date
        existing = Weight.objects.filter(animal=animal, recorded_at=recorded_at)
        if self.instance:  # If updating an existing record, exclude it from duplicates
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                {"non_field_errors": f"A weight record for this animal on {recorded_at} already exists."}
            )

        return data

    def update(self, instance, validated_data):
        # If 'recorded_at' is not in the update request, don't change it
        if 'recorded_at' not in validated_data:
            validated_data['recorded_at'] = instance.recorded_at  # Preserve the old 'recorded_at'

        # Proceed with the update for the other fields
        return super().update(instance, validated_data)
