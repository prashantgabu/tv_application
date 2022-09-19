from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def send_notification(device_id, title, body):
    try:
        device = FCMDevice.objects.filter(device_id=device_id, active=True).first()
        if not device:
            return
        msg = Message(
            notification=Notification(title=title, body=body),
            topic=None,
        )
        result = device.send_message(msg)
        if device:
            print(f"Result for device: {device.registration_id} is - {result}")
        return result
    except Exception as e:
        print(e)
        pass
