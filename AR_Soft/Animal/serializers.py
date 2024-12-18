from rest_framework import serializers
from .models import Animal
from .models import Animal, Group, AnimalGroup

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            'id', 'eartag', 'company', 'race', 'gender', 'room', 'cost', 
            'is_slaughtered', 'feed_cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_slaughtered', 'feed_cost']  # Make 'is_deleted' and 'feed_cost' read-only
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description']

class AnimalGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer()  # Nested Group details
    eartag = serializers.CharField(source='animal.eartag', read_only=True)  # Fetch eartag from Animal model

    class Meta:
        model = AnimalGroup
        fields = ['id', 'animal', 'eartag', 'group', 'assigned_at']
        read_only_fields = ['assigned_at']  # Read-only fields