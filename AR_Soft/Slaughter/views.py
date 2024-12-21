# Slaughter/views.py
from rest_framework import generics
from .models import Slaughter
from .serializers import SlaughterSerializer

class SlaughterListView(generics.ListCreateAPIView):
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer

class SlaughterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer
