# weight/views.py
from rest_framework import generics
from .models import Weight
from .serializers import WeightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from datetime import timedelta


class WeightListView(generics.ListCreateAPIView):
    """
    API view to list all weight records or create a new one.
    Includes filtering by animal_id.
    """
    serializer_class = WeightSerializer

    def get_queryset(self):
        queryset = Weight.objects.all()
        # Optional filtering by animal ID
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        return queryset


class WeightDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific weight record.
    """
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer



class DailyWeightGainView(APIView):
    """
    API view to calculate the daily weight gain of an animal based on its last two weight records.
    """

    def get(self, request, animal_id):
        # Fetch the last two weight records for the given animal, ordered by recorded_at descending
        weights = Weight.objects.filter(animal_id=animal_id).order_by('-recorded_at')[:2]

        # Ensure there are at least two records
        if len(weights) < 2:
            raise NotFound("Not enough weight records to calculate daily weight gain.")

        # Extract the weights and dates
        latest_weight = weights[0]
        previous_weight = weights[1]

        # Calculate the weight difference and days between records
        weight_diff = latest_weight.weight - previous_weight.weight
        days_diff = (latest_weight.recorded_at - previous_weight.recorded_at).days

        if days_diff == 0:
            return Response({"error": "The two records have the same date, cannot calculate daily gain."}, status=400)

        # Calculate the daily weight gain
        daily_gain = weight_diff / days_diff

        return Response({
            "animal_id": animal_id,
            "latest_weight": latest_weight.weight,
            "latest_date": latest_weight.recorded_at,
            "previous_weight": previous_weight.weight,
            "previous_date": previous_weight.recorded_at,
            "weight_diff": weight_diff,
            "days_diff": days_diff,
            "daily_gain": daily_gain
        })
