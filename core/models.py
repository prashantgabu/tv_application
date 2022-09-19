from django.db import models
from django_lifecycle import hook, AFTER_UPDATE, LifecycleModelMixin
from fcm_django.models import FCMDevice

# Create your models here.
from core.helpers import send_notification

DEFAULT_LOCK_NOTE = 'Your Service Is Expired.'


class RemoteDevice(LifecycleModelMixin, models.Model):
    lock = models.BooleanField(default=False)
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
