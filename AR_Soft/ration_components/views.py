from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import RationComponent, RationTable, RationTableComponent
from .serializers import (
    RationComponentSerializer, 
    RationTableSerializer, 
    RationTableComponentSerializer
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

        # If it's bulk, serializer.data is a list of created objects;
        # if it's single, it is just one object. We can unify how we handle logs below.

        # We may need references to the created instances to log changes
        # => the .save() return value can be used if you need the actual model objects.
        # Because we're using `perform_create()`, let's do the logging in there or override it.
        
        # Return a 201 Created response with the created object(s)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    class RationTableViewSet(viewsets.ModelViewSet):
        queryset = RationTable.objects.all()
        serializer_class = RationTableSerializer

        @action(detail=True, methods=['get'])
        def compute_cost(self, request, pk=None):
            """
            Return the cost of a specific RationTable.
            """
            ration_table = self.get_object()
            cost = ration_table.compute_cost()
            return Response({'id': ration_table.id, 'name': ration_table.name, 'cost': cost})
