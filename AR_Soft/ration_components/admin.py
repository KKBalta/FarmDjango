from django.contrib import admin
from .models import RationComponent
from .models import RationTableComponent
from .models import RationComponentChange
from .models import RationTable

admin.site.register(RationTable)
admin.site.register(RationComponent)
admin.site.register(RationTableComponent)
admin.site.register(RationComponentChange)