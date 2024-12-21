from django.shortcuts import render

# Create your views here.
# animal_ration/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AnimalRationLog
from .serializers import AnimalRationLogSerializer
from rest_framework.permissions import IsAuthenticated

class AnimalRationLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing AnimalRationLog entries.
    """
    queryset = AnimalRationLog.objects.all()
    serializer_class = AnimalRationLogSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access these views

    def create(self, request, *args, **kwargs):
        """
        Override create to handle custom logic.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Override update to handle custom logic for ration log transitions.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Custom endpoint to deactivate a specific ration log.
        """
        log = self.get_object()
        if not log.is_active:
            return Response({"detail": "This ration log is already inactive."}, status=status.HTTP_400_BAD_REQUEST)

        log.is_active = False
        log.end_date = request.data.get('end_date')  # Allow setting an end date
        log.save()

        return Response({"detail": "Ration log deactivated successfully."}, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
        Optionally filter logs by animal or ration table.
        """
        queryset = super().get_queryset()
        animal_id = self.request.query_params.get('animal')
        ration_table_id = self.request.query_params.get('ration_table')

        if animal_id:
            queryset = queryset.filter(animal__id=animal_id)
        if ration_table_id:
            queryset = queryset.filter(ration_table__id=ration_table_id)

        return queryset
