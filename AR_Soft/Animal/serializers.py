from rest_framework import serializers
from .models import Animal, Group, AnimalGroup

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            'id', 'eartag', 'company', 'race', 'gender', 'room', 'cost',
            'is_slaughtered', 'feed_cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_slaughtered', 'feed_cost']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description']


class AnimalGroupSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for input but still provide readable output
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())  # Accepts animal ID as input
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())    # Accepts group ID as input
    eartag = serializers.CharField(source='animal.eartag', read_only=True)      # Read eartag from the related animal
    group_details = GroupSerializer(source='group', read_only=True)             # Nested group details for output

    class Meta:
        model = AnimalGroup
        fields = ['id', 'animal', 'eartag', 'group', 'group_details', 'assigned_at']
        read_only_fields = ['assigned_at']
