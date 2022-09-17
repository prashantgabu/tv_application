from django.contrib import admin

from .models import RemoteDevice

admin.site.site_header = "TV Management System"
admin.site.site_title = "TV Management System"
admin.site.index_title = "TV Management System"


@admin.register(RemoteDevice)
class RemoteDeviceAdmin(admin.ModelAdmin):
    list_display = ['mac_address', 'registration_date_time', 'lock']
