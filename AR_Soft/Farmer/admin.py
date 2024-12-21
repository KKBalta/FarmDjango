from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Company  # Import your model
from .models import Farmer  # Import your model

# Register the Company model
admin.site.register(Company)
admin.site.register(Farmer)
