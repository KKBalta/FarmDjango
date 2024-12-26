from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
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

    def update(self, request, *args, **kwargs):
        # Capture the old object before updating
        instance = self.get_object()
        old_values = {
            'price': instance.price,
            'dry_matter': instance.dry_matter,
            'calori': instance.calori,
            'nisasta': instance.nisasta,
        }

        response = super().update(request, *args, **kwargs)

        # Capture the new values from the request
        new_values = request.data

        # Check for changes and log them
        if old_values != {key: new_values.get(key) for key in old_values.keys()}:
            RationComponentChange.objects.create(
                ration_table_component_id=None,  # You can adjust this if you have a ration table component ID to log
                ration_table_name=instance.name,
                component_name=instance.name,
                action='UPDATED',
                old_price=old_values['price'],
                new_price=new_values.get('price', old_values['price']),
                old_dry_matter=old_values['dry_matter'],
                new_dry_matter=new_values.get('dry_matter', old_values['dry_matter']),
                old_calori=old_values['calori'],
                new_calori=new_values.get('calori', old_values['calori']),
                old_nisasta=old_values['nisasta'],
                new_nisasta=new_values.get('nisasta', old_values['nisasta']),
                changed_at=timezone.now()
            )

        return response


class RationTableViewSet(viewsets.ModelViewSet):
    queryset = RationTable.objects.all()
    serializer_class = RationTableSerializer

    @action(detail=True, methods=['get'], url_path='price')
    def table_price(self, request, pk=None):
        """
        Custom action to calculate the total price of a RationTable.
        Endpoint: GET /ration-tables/<pk>/price/
        """
        # 1) Fetch the RationTable
        table = self.get_object()  # uses pk from the URL

        # 2) Get all RationTableComponents linked to this table
        components = RationTableComponent.objects.filter(ration_table=table)

        # 3) Calculate total price (price * quantity)
        total_price = 0
        for item in components:
            total_price += float(item.component.price) * float(item.quantity)

        # 4) Return JSON with the total
        return Response({
            "ration_table_id": table.id,
            "ration_table_name": table.name,
            "total_price": total_price
        })


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

    def perform_create(self, serializer):
        """
        Override perform_create if you need to log *new* RationTableComponents.
        """
        # By default, serializer.save() returns either one instance or a list of instances
        # depending on many=True
        instances = serializer.save()

        # If it's a single create, wrap it in a list for consistent handling
        if not isinstance(instances, list):
            instances = [instances]

        # Log creation in RationComponentChange for each new item
        for instance in instances:
            RationComponentChange.objects.create(
                ration_table_component_id=instance.id,
                ration_table_name=instance.ration_table.name,
                component_name=instance.component.name,
                action='CREATED',
                old_quantity=None,
                new_quantity=instance.quantity,
            )

    def update(self, request, *args, **kwargs):
        # Log changes in RationComponentChange
        instance = self.get_object()
        old_quantity = instance.quantity
        new_quantity = request.data.get('quantity', old_quantity)

        response = super().update(request, *args, **kwargs)

        # Log changes only if the quantity has changed
        if str(old_quantity) != str(new_quantity):
            RationComponentChange.objects.create(
                ration_table_component_id=instance.id,
                ration_table_name=instance.ration_table.name,
                component_name=instance.component.name,
                action='UPDATED',
                old_quantity=old_quantity,
                new_quantity=new_quantity,
            )
        return response

    def destroy(self, request, *args, **kwargs):
        # Log deletion of RationTableComponent
        instance = self.get_object()

        RationComponentChange.objects.create(
            ration_table_component_id=instance.id,
            ration_table_name=instance.ration_table.name,
            component_name=instance.component.name,
            action='DELETED',
            old_quantity=instance.quantity,
            new_quantity=None,
        )

        return super().destroy(request, *args, **kwargs)

class RationComponentChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RationComponentChange.objects.all()
    serializer_class = RationComponentChangeSerializer
