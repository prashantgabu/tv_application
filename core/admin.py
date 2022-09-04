from django.contrib import admin
from .models import RemoteDevice


class RemoteDeviceAdmin(admin.ModelAdmin):
    pass

admin.site.register(RemoteDevice, RemoteDeviceAdmin)
