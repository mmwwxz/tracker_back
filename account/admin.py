from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'about_me', 'avatar',
                    'date_joined', 'last_login', 'subscription_type',
                    'subscription_start', 'is_active', 'telegram_chat_id', 'id', 'unique_link')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'telegram_chat_id', 'account_type')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'about_me',
                                         'subscription_type', 'subscription_start', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
