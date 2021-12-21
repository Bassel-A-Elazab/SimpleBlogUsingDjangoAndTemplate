from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser
from .forms import UserCreationFrom, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationFrom

    list_display = ('email', 'name', 'date_of_birth',
                    'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser')}),
        ('Personal info', {
         'fields': ('name', 'bio', 'date_of_birth', 'picture')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff',
         'is_superuser', 'password1', 'password2')}),
        ('Personal info', {
         'fields': ('name', 'bio', 'date_of_birth', 'picture')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    ordering = ('email', )


admin.site.register(MyUser, UserAdmin)
