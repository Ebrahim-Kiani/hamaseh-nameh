from django.contrib import admin
from .models import User, DiscountCode, Address
# Register your models here.

class AdminUser(admin.ModelAdmin):

    list_display = [ 'email', 'full_name','is_active', 'phone_number']
    list_filter = ['is_staff','is_active' ]


class AdminDiscountCode(admin.ModelAdmin):
    list_display = [ 'discount_percent', 'code','is_valid']
    list_filter = ['discount_percent']


class AdminAddress(admin.ModelAdmin):
    list_display = ['user','province','city']
    list_filter = ['city']


admin.site.register(User, AdminUser)
admin.site.register(DiscountCode, AdminDiscountCode)
admin.site.register(Address, AdminAddress)