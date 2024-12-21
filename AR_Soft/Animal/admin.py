from django.contrib import admin

from .models import Animal  # Import your model
from .models import Group,AnimalGroup
# Register the Company model
admin.site.register(Animal)
admin.site.register(Group)
admin.site.register(AnimalGroup)


