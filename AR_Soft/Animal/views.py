# animal/views.py
from rest_framework import generics
from .models import Animal
from .serializers import AnimalSerializer

class AnimalListView(generics.ListCreateAPIView):
    """
    API view to list all animals or create a new one.
    Includes filtering by company_id, race, and gender.
    """
    serializer_class = AnimalSerializer

    def get_queryset(self):
        # Start with all animals
        queryset = Animal.objects.all()

        # Filter by company_id if provided
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)

        # Filter by race if provided (case-insensitive match)
        race = self.request.query_params.get('race')
        if race:
            queryset = queryset.filter(race__iexact=race)

        # Filter by gender if provided (convert 0/1 to Boolean)
        gender = self.request.query_params.get('gender')
        if gender is not None:
            try:
                gender_bool = bool(int(gender))  # Convert '0' or '1' to a Boolean
                queryset = queryset.filter(gender=gender_bool)
            except ValueError:
                pass  # Ignore invalid gender filter

        return queryset


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific animal by ID.
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
