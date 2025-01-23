from django.contrib import admin
from .models import Vaccine, AnimalVaccineRecord

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'created_at']

@admin.register(AnimalVaccineRecord)
class AnimalVaccineRecordAdmin(admin.ModelAdmin):
    list_display = ['animal', 'vaccine', 'date_administered', 'administered_by']
    list_filter = ['date_administered']
    search_fields = ['animal__eartag', 'vaccine__name']
