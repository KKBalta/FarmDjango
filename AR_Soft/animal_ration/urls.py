# animal_ration/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalRationLogViewSet

# Create a router and register the AnimalRationLogViewSet
router = DefaultRouter()
router.register(r'animal-ration-logs', AnimalRationLogViewSet, basename='animal-ration-log')

# Define the app-specific URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
