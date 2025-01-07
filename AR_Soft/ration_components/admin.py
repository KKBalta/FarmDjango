from django.contrib import admin
from .models import RationComponent, RationTable, RationTableComponent

class SoftDeleteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Include all objects (active and soft-deleted)
        return self.model.all_objects.all()

    def is_deleted(self, obj):
        return obj.is_deleted()
    is_deleted.boolean = True  # Show a boolean icon in the admin panel
    is_deleted.short_description = "Deleted?"

    list_display = ('__str__', 'is_deleted', 'updated_at', 'deleted_at')
    list_filter = ('deleted_at',)  # Add a filter for soft-deleted records

    actions = ['restore_selected']

    def restore_selected(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted():
                obj.restore()
        self.message_user(request, "Selected objects have been restored.")
    restore_selected.short_description = "Restore selected soft-deleted records"

# Register the models with the customized admin class
@admin.register(RationComponent)
class RationComponentAdmin(SoftDeleteAdmin):
    pass

@admin.register(RationTable)
class RationTableAdmin(SoftDeleteAdmin):
    pass

@admin.register(RationTableComponent)
class RationTableComponentAdmin(SoftDeleteAdmin):
    pass
