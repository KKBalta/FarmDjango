# weight/serializers.py
from rest_framework import serializers
from .models import Weight

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['id', 'animal', 'weight', 'recorded_at']
        read_only_fields = ['recorded_at']  # Prevent changes to the recorded_at date after creation

    def validate(self, data):
        # Check for duplicate records for the same animal and recorded_at
        animal = data.get('animal')
        recorded_at = self.instance.recorded_at if self.instance else data.get('recorded_at')

        existing = Weight.objects.filter(animal=animal, recorded_at=recorded_at)
        if self.instance:
            # Exclude the current record being updated from the validation check
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                f"A weight record for this animal on {recorded_at} already exists."
            )

        return data
z