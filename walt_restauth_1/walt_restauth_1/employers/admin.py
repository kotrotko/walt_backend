from django.contrib import admin

from .models import Employer

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name',)

admin.site.register(Employer, EmployerAdmin)
