from django.db import models
from django_lifecycle import hook, AFTER_UPDATE, LifecycleModelMixin
from fcm_django.models import FCMDevice

# Create your models here.
from core.helpers import send_notification

DEFAULT_LOCK_NOTE = 'Your Service Is Expired.'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class RemoteDevice(LifecycleModelMixin, models.Model):
    lock = models.BooleanField(default=True)
    mac_address = models.CharField(max_length=300, null=True, blank=True, verbose_name="MAC Address", unique=True)
    note = models.TextField(default=DEFAULT_LOCK_NOTE)
    registration_date_time = models.DateTimeField(null=True, blank=True)
    device = models.OneToOneField(FCMDevice, on_delete=models.SET_NULL, related_name="remote_device", null=True,
                                  blank=True)

    @hook(AFTER_UPDATE, when='lock', has_changed=True)
    def after_lock_update(self):
        title = "New Lock Notification"

        if not self.lock:
            body = "Device is unlocked"
        else:
            body = "Device is locked"
        if self.device:
            send_notification(self.device.device_id, title, body)

    def __str__(self):
        return self.mac_address

    # def save(self, *args, **kwargs):
    #     super(RemoteDevice, self).save(*args, **kwargs)
    #     if self.pk:
    #         pass
    #     else:
    #         pass
    #     data = {
    #         "action": "lock",
    #         "bundle": {
    #             "lock": self.lock,
    #             "note": self.note,
    #         }
    #     }
    # self.device.send_message(data={"data": json.dumps(data)})


class AppVersion(LifecycleModelMixin, BaseModel):
    version_no = models.CharField(max_length=300, verbose_name="App Version No.", unique=True)
    app_file = models.FileField(upload_to="app_versions/")
    mandatory_update = models.BooleanField(default=False)

    def __str__(self):
        return self.version_no

    class Meta:
        ordering = ['-id']
