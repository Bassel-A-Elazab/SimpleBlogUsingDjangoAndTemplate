from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationFrom
from .models import MyUser


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationFrom

    list_display = ("email", "name", "date_of_birth", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "is_staff", "is_superuser", "is_active")}),
        ("Personal info", {"fields": ("name", "bio", "date_of_birth", "picture")}),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "password1",
                    "password2",
                )
            },
        ),
        ("Personal info", {"fields": ("name", "bio", "date_of_birth", "picture")}),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )

    ordering = ("email",)


admin.site.register(MyUser, UserAdmin)
