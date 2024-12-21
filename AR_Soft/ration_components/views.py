# ration_components/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import RationComponent, RationTable, RationTableComponent, RationComponentChange
from .serializers import (
    RationComponentSerializer, 
    RationTableSerializer, 
    RationTableComponentSerializer, 
    RationComponentChangeSerializer
)

class RationComponentViewSet(viewsets.ModelViewSet):
    queryset = RationComponent.objects.all()
    serializer_class = RationComponentSerializer

class RationTableViewSet(viewsets.ModelViewSet):
    queryset = RationTable.objects.all()
    serializer_class = RationTableSerializer

class RationTableComponentViewSet(viewsets.ModelViewSet):
    queryset = RationTableComponent.objects.all()
    serializer_class = RationTableComponentSerializer

    def update(self, request, *args, **kwargs):
        # Log changes in RationComponentChange
        instance = self.get_object()
        old_quantity = instance.quantity
        new_quantity = request.data.get('quantity', old_quantity)

        response = super().update(request, *args, **kwargs)

        if str(old_quantity) != str(new_quantity):  # Only log if quantity changes
            RationComponentChange.objects.create(
                ration_table_component=instance,
                old_quantity=old_quantity,
                new_quantity=new_quantity
            )

        return response

class RationComponentChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RationComponentChange.objects.all()
    serializer_class = RationComponentChangeSerializer
