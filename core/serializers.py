from rest_framework.serializers import ModelSerializer

from core.models import RemoteDevice, AppVersion


class RemoteDeviceSerializer(ModelSerializer):
    class Meta:
        model = RemoteDevice
        fields = "__all__"


class AppVersionSerializer(ModelSerializer):
    class Meta:
        model = AppVersion
        exclude = ["updated_at", "created_at", "id"]
