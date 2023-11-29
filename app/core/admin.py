"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for admins"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # each bracket is a section
        # first arg is the title of the section
        # second arg is a dictionary of fields to be included in the section
        # the password field is automatically encrypted
        (
            _('Personal Info'),
            {'fields': ('name',)}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        # the last section is the important one
        # it contains the permissions that are available to the user
        (
            _('Important dates'),
            {'fields': ('last_login',)}
        )
    )
    # this is to make the last_login field read-only
    readonly_fields = ['last_login', ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # this is to make the input fields wider
            'fields': ('email',
                       'password1',
                       'password2',
                       'name',
                       'is_active',
                       'is_staff',
                       'is_superuser')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
