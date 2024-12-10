from django.contrib import admin
from .models import ContactUs, UserMessages


# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_awnsered']
    list_editable = ['is_awnsered', ]


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(UserMessages, MessagesAdmin)

