from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'secret_question', 'secret_answer')
    search_fields = ('username',)
    readonly_fields = ('id',)
    ordering = ('username',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Secret Info', {'fields': ('secret_question', 'secret_answer')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
