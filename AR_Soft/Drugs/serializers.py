from rest_framework import serializers
from .models import Vaccine, AnimalVaccineRecord

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'


class AnimalVaccineRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalVaccineRecord
        fields = '__all__'
