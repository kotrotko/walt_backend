from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'password', 'is_staff', 'roles')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {
            'fields': ('email',
                'password',
                )
        }),
        ('Roles', {'fields': ('roles',)}),  # Add roles fieldset
    )
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
