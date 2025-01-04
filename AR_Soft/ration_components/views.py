from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import RationComponent, RationTable, RationTableComponent
from .serializers import (
    RationComponentSerializer, 
    RationTableSerializer, 
    RationTableComponentSerializer
)

class RationComponentViewSet(viewsets.ModelViewSet):
    queryset = RationComponent.objects.all()  # Default to ActiveManager
    serializer_class = RationComponentSerializer

    def get_queryset(self):
        # Return only active records
        return RationComponent.objects.filter(deleted_at__isnull=True)
    
    def get_object(self):
        # Use all_objects for actions that require access to soft-deleted records
        if self.action in ['restore', 'hard_delete']:
            return RationComponent.all_objects.get(pk=self.kwargs['pk'])
        return super().get_object()
    
    @action(detail=False, methods=['get'], url_path='soft-deleted')
    def get_soft_deleted(self, request):
        """
        Get a list of all soft-deleted RationComponents.
        """
        soft_deleted_components = RationComponent.all_objects.filter(deleted_at__isnull=False)
        serializer = self.get_serializer(soft_deleted_components, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Restore a soft-deleted RationComponent.
        """
        component = self.get_object()
        if component.is_deleted():
            component.restore()
            return Response({'status': 'restored'}, status=status.HTTP_200_OK)
        return Response({'status': 'not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='hard-delete')
    def hard_delete(self, request, pk=None):
        """
        Permanently delete a soft-deleted RationComponent.
        """
        component = self.get_object()  # Fetches using all_objects
        if component.is_deleted():
            print(component.is_deleted())
            component.delete(hard_delete=True)  # Trigger hard delete
            return Response({'status': 'hard deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'not soft deleted'}, status=status.HTTP_400_BAD_REQUEST)

class RationTableViewSet(viewsets.ModelViewSet):
    queryset = RationTable.objects.all()
    serializer_class = RationTableSerializer

    def get_queryset(self):
        # Return only active records
        return RationTable.objects.filter(deleted_at__isnull=True)
    
    def get_object(self):
        # Use all_objects for actions that require access to soft-deleted records
        if self.action in ['restore', 'hard_delete']:
            return RationTable.all_objects.get(pk=self.kwargs['pk'])
        return super().get_object()

    @action(detail=False, methods=['get'], url_path='soft-deleted')
    def get_soft_deleted(self, request):
        """
        Get a list of all soft-deleted RationTables.
        """
        soft_deleted_tables = RationTable.all_objects.filter(deleted_at__isnull=False)
        serializer = self.get_serializer(soft_deleted_tables, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Restore a soft-deleted RationTable.
        """
        table = self.get_object()
        if table.is_deleted():
            table.restore()
            return Response({'status': 'restored'}, status=status.HTTP_200_OK)
        return Response({'status': 'not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='hard-delete')
    def hard_delete(self, request, pk=None):
        """
        Permanently delete a soft-deleted RationTable.
        """
        table = self.get_object()  # Fetches using all_objects
        if table.is_deleted():
            table.delete(hard_delete=True)  # Trigger hard delete
            return Response({'status': 'hard deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'not soft deleted'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='compute-cost')
    def compute_cost(self, request, pk=None):
        """
        Recalculate and return the cost of a specific RationTable.
        """
        ration_table = self.get_object()
        cost = ration_table.compute_cost()
        return Response({'id': ration_table.id, 'name': ration_table.name, 'cost': cost})

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import RationTableComponent
from .serializers import RationTableComponentSerializer


class RationTableComponentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing RationTableComponent instances.
    """
    queryset = RationTableComponent.objects.all()
    serializer_class = RationTableComponentSerializer

    def get_queryset(self):
        """
        Override to return only active (non-soft-deleted) records by default.
        """
        return RationTableComponent.objects.filter(deleted_at__isnull=True)

    def get_object(self):
        """
        Retrieve an object, including soft-deleted ones for certain actions.
        """
        if self.action in ['restore', 'hard_delete']:
            # Use all_objects manager to include soft-deleted records
            return get_object_or_404(RationTableComponent.all_objects, pk=self.kwargs['pk'])
        # Default behavior for other actions
        return super().get_object()

    @action(detail=False, methods=['get'], url_path='soft-deleted')
    def get_soft_deleted(self, request):
        """
        Get a list of all soft-deleted RationTableComponents.
        """
        soft_deleted_components = RationTableComponent.all_objects.filter(deleted_at__isnull=False)
        serializer = self.get_serializer(soft_deleted_components, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Restore a soft-deleted RationTableComponent.
        """
        component = self.get_object()
        if component.is_deleted():
            component.restore()
            return Response({'status': 'restored'}, status=status.HTTP_200_OK)
        return Response({'status': 'not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='hard-delete')
    def hard_delete(self, request, pk=None):
        """
        Permanently delete a soft-deleted RationTableComponent.
        """
        component = self.get_object()  # Fetches using all_objects
        if component.is_deleted():
            component.delete(hard_delete=True)  # Trigger hard delete
            return Response({'status': 'hard deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'not soft deleted'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Override create to handle both single and bulk creation of RationTableComponents.
        """
        # Check if the incoming data is a list (bulk create)
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Single record
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return a 201 Created response with the created object(s)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
