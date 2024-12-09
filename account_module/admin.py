from django.contrib import admin
from .models import User, DiscountCode, Address
# Register your models here.

class AdminUser(admin.ModelAdmin):

    list_display = [ 'full_name', 'is_active', 'phone']
    list_filter = ['is_staff', 'is_active']


class AdminDiscountCode(admin.ModelAdmin):
    list_display = ['discount_percent', 'code', 'is_valid']
    list_filter = ['discount_percent']


class AdminAddress(admin.ModelAdmin):
    list_display = ['user','province','city']
    list_filter = ['city']



admin.site.register(DiscountCode, AdminDiscountCode)
admin.site.register(Address, AdminAddress)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User  # Import your custom user model

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin
    list_display = ('phone', 'is_active', 'is_staff')
    search_fields = ('phone',)

    # Fields shown when editing a user
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    ordering = ('phone',)

    # Add the password change option
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<id>/password/', self.admin_site.admin_view(self.user_change_password), name='auth_user_password_change'),
        ]
        return custom_urls + urls

admin.site.unregister(Group)