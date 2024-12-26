# ration_components/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RationComponentViewSet, 
    RationTableViewSet, 
    RationTableComponentViewSet, 
    RationComponentChangeViewSet
)

router = DefaultRouter()
router.register(r'ration-components', RationComponentViewSet, basename='ration-component')
router.register(r'ration-tables', RationTableViewSet, basename='ration-table')
router.register(r'ration-table-components', RationTableComponentViewSet, basename='ration-table-component')
router.register(r'ration-component-changes', RationComponentChangeViewSet, basename='ration-component-change')


urlpatterns = [
    path('', include(router.urls)),
]
