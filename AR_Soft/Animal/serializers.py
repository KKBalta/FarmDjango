# animal/serializers.py
from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            'id', 'eartag', 'company', 'race', 'gender', 'room', 'cost', 
            'is_deleted', 'feed_cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']  # Prevent client from modifying these
