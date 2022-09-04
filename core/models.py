from django.db import models
from fcm_django.models import FCMDevice
import json

# Create your models here.
DEFAULT_LOCK_NOTE = 'Your Service Is Expired.'


class RemoteDevice(models.Model):
    lock = models.BooleanField(default=True)
    device = models.ForeignKey(FCMDevice, on_delete=models.CASCADE)
    note = models.TextField(default=DEFAULT_LOCK_NOTE, null=True)
    mac_address = models.CharField(max_length=300, null=True, blank=True, verbose_name="MAC Address", unique=True)

    def __str__(self):
        if self.device:
            if self.device.name:
                return self.device.name + ' ' + '(' + self.device.device_id + ')'
            else:
                return self.device.device_id
        return 'Unknown Device' + ' ' + '(' + self.id + ')'

    def save(self, *args, **kwargs):
        super(RemoteDevice, self).save(*args, **kwargs)
        if self.pk:
            # existed
            pass
        else:
            # new
            pass
        data = {
            "action": "lock",
            "bundle": {
                "lock": self.lock,
                "note": self.note,
            }
        }
        self.device.send_message(data={"data": json.dumps(data)})
