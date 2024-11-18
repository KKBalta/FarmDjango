# weight/admin.py
from django.contrib import admin
from .models import Weight

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('animal', 'weight', 'recorded_at')
    list_filter = ('animal', 'recorded_at')
    search_fields = ('animal__eartag',)
