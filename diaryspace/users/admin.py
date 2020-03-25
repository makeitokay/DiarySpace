from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname', 'patronymic')
    list_filter = ('is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['codename', 'name', 'content_type']


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
