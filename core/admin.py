from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']


admin.site.register(User, UserAdmin)