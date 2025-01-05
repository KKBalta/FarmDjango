from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentChangeLogViewSet, RationTableLogViewSet, RationTableComponentLogViewSet

router = DefaultRouter()
router.register(r'component-change-logs', ComponentChangeLogViewSet, basename='component-change-log')
router.register(r'ration-table-logs', RationTableLogViewSet, basename='ration-table-log')
router.register(r'ration-table-component-logs', RationTableComponentLogViewSet, basename='ration-table-component-log')

urlpatterns = [
    path('', include(router.urls)),
]
