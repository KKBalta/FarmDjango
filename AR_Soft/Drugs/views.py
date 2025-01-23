from rest_framework.viewsets import ModelViewSet
from .models import Vaccine, AnimalVaccineRecord
from .serializers import VaccineSerializer, AnimalVaccineRecordSerializer

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

class AnimalVaccineRecordViewSet(ModelViewSet):
    queryset = AnimalVaccineRecord.objects.all()
    serializer_class = AnimalVaccineRecordSerializer
