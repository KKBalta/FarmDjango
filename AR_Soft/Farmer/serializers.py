from rest_framework import serializers
from .models import Farmer, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']

class FarmerSerializer(serializers.ModelSerializer):
    company = CompanySerializer()  # Nested serializer

    class Meta:
        model = Farmer
        fields = ['id', 'name', 'birth_date', 'position', 'email', 'phone', 'company']

    def create(self, validated_data):
        company_data = validated_data.pop('company')  # Extract company data
        company, created = Company.objects.get_or_create(**company_data)  # Create or get Company
        farmer = Farmer.objects.create(company=company, **validated_data)  # Create Farmer
        return farmer

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)  # Extract company data
        if company_data:
            # Update company data
            Company.objects.filter(pk=instance.company.pk).update(**company_data)

        # Update farmer instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance