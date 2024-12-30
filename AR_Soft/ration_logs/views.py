from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ComponentChangeLog, RationTableLog, RationTableComponentLog
from .serializers import ComponentChangeLogSerializer, RationTableLogSerializer, RationTableComponentLogSerializer
from rest_framework.viewsets import ModelViewSet
from ration_components.models import RationComponent
from ration_components.serializers import RationComponentSerializer

# ViewSet for ComponentChangeLog
class ComponentChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentChangeLog.objects.all().order_by('-changed_at')
    serializer_class = ComponentChangeLogSerializer

    @action(detail=False, methods=['get'], url_path='component/(?P<component_id>[^/.]+)')
    def logs_by_component(self, request, component_id=None):
        logs = self.queryset.filter(component_id=component_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

# ViewSet for RationTableLog
class RationTableLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RationTableLog.objects.all().order_by('-changed_at')
    serializer_class = RationTableLogSerializer

    @action(detail=False, methods=['get'], url_path='table/(?P<table_id>[^/.]+)')
    def logs_by_table(self, request, table_id=None):
        logs = self.queryset.filter(ration_table_id=table_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

# ViewSet for RationTableComponentLog
class RationTableComponentLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RationTableComponentLog.objects.all().order_by('-changed_at')
    serializer_class = RationTableComponentLogSerializer

    @action(detail=False, methods=['get'], url_path='table-component/(?P<component_id>[^/.]+)')
    def logs_by_table_component(self, request, component_id=None):
        logs = self.queryset.filter(table_component_id=component_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='ration-table/(?P<ration_table_id>[^/.]+)')
    def logs_by_ration_table(self, request, ration_table_id=None):
        logs = self.queryset.filter(table_component__ration_table_id=ration_table_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

class ArchivedRationComponentViewSet(ModelViewSet):
    queryset = RationComponent.all_objects.filter(deleted_at__isnull=False)
    serializer_class = RationComponentSerializer