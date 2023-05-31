from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from account.models import User
from django.utils.translation import gettext_lazy as _


@register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', "is_active", 'date_joined')
    search_fields = ('username', 'email')

    fieldsets = (
        (_("Personal info"), {"fields": ("username", "email", "avatar")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    actions = ['activate_selected_user', 'deactivate_selected_user']

    def deactivate_selected_user(self, request, queryset):
        queryset.update(is_active=False)

    def activate_selected_user(self, request, queryset):
        queryset.update(is_active=True)

