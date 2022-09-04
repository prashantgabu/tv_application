from rest_framework.serializers import ModelSerializer

from core.models import RemoteDevice


class RemoteDeviceSerializer(ModelSerializer):
    class Meta:
        model = RemoteDevice
        fields = "__all__"
