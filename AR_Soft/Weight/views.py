# weight/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Weight
from .serializers import WeightSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from Animal.models import Group, Animal

from django.shortcuts import get_object_or_404

class WeightListView(generics.ListCreateAPIView):
    """
    API view to list all weight records or create a new one (or multiple).
    Includes filtering by animal_id.
    """
    serializer_class = WeightSerializer

    def get_queryset(self):
        queryset = Weight.objects.all()
        # Optional filtering by animal ID
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)

        eartag = self.request.query_params.get('eartag')
        if eartag:
            queryset = queryset.filter(animal__eartag=eartag)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Override create to handle both single and bulk creation of Weight records.
        """
        # If the request data is a list => bulk create
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Single record
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            return Response(
                {"error": "The two records have the same date, cannot calculate daily gain."},
                status=400
            )

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


class AllWeightGainView(APIView):
    """
    API view to calculate the gain ratios (daily or monthly) 
    for *all* consecutive weight records of an animal.
    """

    def get(self, request, animal_id):
        # Fetch ALL weight records for the given animal, ascending by date
        weights = Weight.objects.filter(animal_id=animal_id).order_by('recorded_at')

        # If there's only one record or none, can't compute a difference
        if len(weights) < 2:
            raise NotFound("Not enough weight records to calculate weight gain history.")

        # Prepare a list to hold each pair's gain data
        gain_history = []

        # Loop through consecutive pairs: (weights[i], weights[i+1])
        for i in range(len(weights) - 1):
            current_weight = weights[i]
            next_weight = weights[i + 1]

            weight_diff = next_weight.weight - current_weight.weight
            days_diff = (next_weight.recorded_at - current_weight.recorded_at).days

            # Handle edge case if records share the same day
            if days_diff == 0:
                daily_gain = None  # or skip, or handle differently
            else:
                daily_gain = weight_diff / days_diff

            # You can also do monthly gain if you want to interpret "30 days" as a month
            # monthly_gain = daily_gain * 30  # approximate, if desired

            gain_history.append({
                "start_date": current_weight.recorded_at,
                "start_weight": current_weight.weight,
                "end_date": next_weight.recorded_at,
                "end_weight": next_weight.weight,
                "weight_diff": weight_diff,
                "days_diff": days_diff,
                "daily_gain": daily_gain
                # "monthly_gain": monthly_gain,  # if you want it
            })

        return Response({
            "animal_id": animal_id,
            "records_count": len(weights),
            "gain_history": gain_history
        })

class GroupDailyGainView(APIView):
    """
    Returns daily weight gain info for *each* animal in a given group,
    using only the *last two* weight records per animal.
    Also calculates the group's average daily gain rate.
    """

    def get(self, request, group_id):
        # 1) Validate the group actually exists
        group = get_object_or_404(Group, pk=group_id)

        # 2) Find all animals in this group
        animals_in_group = Animal.objects.filter(animal_groups__group=group).distinct()

        # 3) Prepare a list to hold the results
        daily_gains = []
        total_gain = 0
        valid_animals_count = 0

        for animal in animals_in_group:
            # 4) Get the last two Weight records for this animal
            weights = (Weight.objects
                       .filter(animal=animal)
                       .order_by('-recorded_at')[:2])

            # If fewer than 2 records, we can't compute daily gain
            if len(weights) < 2:
                continue

            latest_weight = weights[0]
            previous_weight = weights[1]

            weight_diff = latest_weight.weight - previous_weight.weight
            days_diff = (latest_weight.recorded_at - previous_weight.recorded_at).days

            if days_diff == 0:
                daily_gain = None
            else:
                daily_gain = weight_diff / days_diff
                total_gain += daily_gain  # Add to total gain for average calculation
                valid_animals_count += 1

            # Append individual animal's daily gain info
            daily_gains.append({
                "animal_id": animal.id,
                "eartag": animal.eartag,
                "latest_weight": latest_weight.weight,
                "latest_date": latest_weight.recorded_at,
                "previous_weight": previous_weight.weight,
                "previous_date": previous_weight.recorded_at,
                "weight_diff": weight_diff,
                "days_diff": days_diff,
                "daily_gain": daily_gain
            })

        # Calculate group average daily gain
        group_average_gain = total_gain / valid_animals_count if valid_animals_count > 0 else None

        # Return the aggregated data
        return Response({
            "group_id": group_id,
            "group_name": group.name,
            "animals_count": animals_in_group.count(),
            "gains_count": len(daily_gains),  # how many animals had 2+ records
            "group_average_daily_gain": group_average_gain,  # Average daily gain for the group
            "results": daily_gains
        })

class GroupAllWeightGainView(APIView):
    """
    Returns *all* consecutive weight gains for each animal in a given group.
    Similar to 'AllWeightGainView', but done *per animal* in that group.
    Also calculates the group's average daily gain rate over all records.
    """

    def get(self, request, group_id):
        # 1) Ensure the group exists
        group = get_object_or_404(Group, pk=group_id)

        # 2) Get all animals in the group (unique, just in case)
        animals_in_group = Animal.objects.filter(animal_groups__group=group).distinct()

        group_gains = []
        total_gain = 0
        total_days = 0

        for animal in animals_in_group:
            # 3) Fetch *all* weight records for this animal, sorted ascending
            weights = Weight.objects.filter(animal=animal).order_by('recorded_at')

            if len(weights) < 2:
                group_gains.append({
                    "animal_id": animal.id,
                    "eartag": animal.eartag,
                    "records_count": len(weights),
                    "gain_history": []
                })
                continue

            gain_history = []
            for i in range(len(weights) - 1):
                current_weight = weights[i]
                next_weight = weights[i + 1]

                weight_diff = next_weight.weight - current_weight.weight
                days_diff = (next_weight.recorded_at - current_weight.recorded_at).days

                daily_gain = None
                if days_diff != 0:
                    daily_gain = weight_diff / days_diff
                    total_gain += daily_gain
                    total_days += days_diff

                gain_history.append({
                    "start_date": current_weight.recorded_at,
                    "start_weight": current_weight.weight,
                    "end_date": next_weight.recorded_at,
                    "end_weight": next_weight.weight,
                    "weight_diff": weight_diff,
                    "days_diff": days_diff,
                    "daily_gain": daily_gain
                })

            group_gains.append({
                "animal_id": animal.id,
                "eartag": animal.eartag,
                "records_count": len(weights),
                "gain_history": gain_history
            })

        # Calculate group average daily gain
        group_average_gain = total_gain / total_days if total_days > 0 else None

        # Return the final JSON
        return Response({
            "group_id": group_id,
            "group_name": group.name,
            "animals_count": animals_in_group.count(),
            "group_average_daily_gain": group_average_gain,  # Average daily gain for the group
            "results": group_gains
        })
