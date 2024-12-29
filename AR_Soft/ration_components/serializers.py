from rest_framework import serializers
from .models import RationComponent, RationTable, RationTableComponent

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
    cost = serializers.SerializerMethodField()

    class Meta:
        model = RationTable
        fields = ['id', 'name', 'description', 'cost']

    def get_cost(self, obj):
        return obj.compute_cost()
