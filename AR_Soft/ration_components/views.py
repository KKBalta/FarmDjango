from rest_framework import viewsets, status
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


class RationTableComponentViewSet(viewsets.ModelViewSet):
    queryset = RationTableComponent.objects.all()
    serializer_class = RationTableComponentSerializer

    def update(self, request, *args, **kwargs):
        # Log changes in RationComponentChange
        instance = self.get_object()
        old_quantity = instance.quantity
        new_quantity = request.data.get('quantity', old_quantity)

        response = super().update(request, *args, **kwargs)

        # Log changes only if the quantity has been updated
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
