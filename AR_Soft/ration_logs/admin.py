from django.contrib import admin
from .models import ComponentChangeLog, RationTableLog, RationTableComponentLog

@admin.register(ComponentChangeLog)
class ComponentChangeLogAdmin(admin.ModelAdmin):
    list_display = ('component', 'field_name', 'old_value', 'new_value', 'changed_at')

@admin.register(RationTableLog)
class RationTableLogAdmin(admin.ModelAdmin):
    list_display = ('ration_table', 'action', 'changed_at')

@admin.register(RationTableComponentLog)
class RationTableComponentLogAdmin(admin.ModelAdmin):
    list_display = ('table_component', 'action', 'old_quantity', 'new_quantity', 'changed_at')
