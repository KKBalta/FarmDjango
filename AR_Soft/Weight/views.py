# weight/views.py
from rest_framework import generics
from .models import Weight
from .serializers import WeightSerializer

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
