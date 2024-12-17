# weight/serializers.py
from rest_framework import serializers
from .models import Weight
from datetime import date

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['id', 'animal', 'weight', 'recorded_at']

    def validate(self, data):
        # Validate that there are no duplicate records for the same animal and recorded_at date
        animal = data.get('animal')
        recorded_at = data.get('recorded_at')
        
        if recorded_at > date.today():
            raise serializers.ValidationError(
                "The recorded date cannot be in the future."
            )
        existing = Weight.objects.filter(animal=animal, recorded_at=recorded_at)
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                f"A weight record for this animal on {recorded_at} already exists."
            )

        return data
