from rest_framework import serializers
from .models import Slaughter
from datetime import datetime, date

class SlaughterSerializer(serializers.ModelSerializer):
    profit = serializers.SerializerMethodField()
    feed_cost = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = Slaughter
        fields = ['id', 'animal', 'date', 'carcas_weight', 'sale_price', 'kdv', 'profit', 'feed_cost', 'cost']

    def get_profit(self, obj):
        return obj.calculate_profit()

    def get_feed_cost(self, obj):
        """
        Retrieve the feed_cost from the related Animal model.
        """
        return obj.animal.feed_cost if obj.animal else None

    def get_cost(self, obj):
        """
        Retrieve the cost from the related Animal model.
        """
        return obj.animal.cost if obj.animal else None

    # Validation for carcass weight
    def validate_carcas_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Carcass weight must be a positive number.")
        return value

    # Validation for sale price
    def validate_sale_price(self, value):
        if value is None:
            raise serializers.ValidationError("Sale price cannot be null.")
        if value <= 0:
            raise serializers.ValidationError("Sale price must be a positive number.")
        return value

    # Default KDV value
    def create(self, validated_data):
        validated_data.setdefault('kdv', 0.0)  # Default KDV to 0.0 if not provided
        return super().create(validated_data)
