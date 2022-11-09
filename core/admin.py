from django.contrib import admin

from .models import RemoteDevice, AppVersion

admin.site.site_header = "TV Management System"
admin.site.site_title = "TV Management System"
admin.site.index_title = "TV Management System"


@admin.register(RemoteDevice)
class RemoteDeviceAdmin(admin.ModelAdmin):
    list_display = ['mac_address', 'registration_date_time', 'lock']


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ['version_no', 'app_file', 'mandatory_update']
