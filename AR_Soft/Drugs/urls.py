from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet, AnimalVaccineRecordViewSet

router = DefaultRouter()
router.register('vaccines', VaccineViewSet)
router.register('vaccine-records', AnimalVaccineRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
