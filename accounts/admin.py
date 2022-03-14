from accounts.models import CustomUser
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (_('Basic Details'), {
            'fields': ('name', 'email', 'contact_number', 'dob', 'profile_pic', 'password', 'street', 'city', 'state', 'pincode', 'country')
         }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
            }),
    )
    add_fieldsets = (
        (_('Basic Details'), {
            'classes': ('wide',),
            'fields': ('name', 'email', 'contact_number', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'contact_number', 'is_staff',)
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
