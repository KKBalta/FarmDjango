# Slaughter/views.py
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Slaughter
from .serializers import SlaughterSerializer

class SlaughterViewSet(ModelViewSet):
    """
    ViewSet for Slaughter model. Includes list, create, retrieve, update, and delete operations,
    as well as a custom endpoint for calculating total profit.
    """
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer


class SlaughterListView(generics.ListCreateAPIView):
    """
    List and create Slaughter records.
    """
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer


class SlaughterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single Slaughter record.
    """
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer
