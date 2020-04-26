from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from .models import User


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "name", "surname", "patronymic", "school")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "name", "surname", "patronymic")
    list_filter = ("is_admin", "groups__name", "is_active")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    fieldsets = (
        (None, {"fields": ("email", "password", "school")}),
        ("Personal info", {"fields": ("name", "surname", "patronymic",)}),
        ("Permissions", {"fields": ("is_admin",)}),
        ("Active", {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "surname",
                    "patronymic",
                    "school",
                    "groups",
                ),
            },
        ),
    )


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ["codename", "name", "content_type"]


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
