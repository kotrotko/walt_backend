from django.contrib import admin

from .models import JobSeeker

class JobseekerAdmin(admin.ModelAdmin):
    list_display = ('first_name',)

admin.site.register(JobSeeker, JobseekerAdmin)
