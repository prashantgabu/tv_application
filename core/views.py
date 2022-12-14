import os
from http import HTTPStatus
from time import timezone

from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RemoteDevice, AppVersion
from .serializers import AppVersionSerializer


# Create your views here.


@csrf_exempt
def download_updates(request, *args, **kwargs):
    checksum = request.GET.get('checksum')
    if checksum:
        if len(checksum) == 33:
            file_path = settings.RAW_FILES_DIR + '/' + checksum
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/pdf")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response

        file_path = settings.RAW_FILES_DIR + '/' + checksum
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.android.package-archive'")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    raise Http404


@csrf_exempt
def check_updates(request, *args, **kwargs):
    return JsonResponse(settings.LATEST_APK_INFO)


@csrf_exempt
def device_register(request, *args, **kwargs):
    status = HTTPStatus.OK

    device_id = request.POST.get('device_id')
    registration_id = request.POST.get('registration_id')
    type = request.POST.get('type', 'android')
    mac_address = request.POST.get('mac_address')
    name = request.POST.get('name')

    if not device_id or not registration_id or not name or not type or not mac_address:
        status = HTTPStatus.BAD_REQUEST
        return HttpResponse(status.phrase, status=status.value)

    device = FCMDevice.objects.filter(device_id=device_id).first()
    if not device:
        # create new
        device = FCMDevice.objects.create(device_id=device_id, type=type,
                                          registration_id=registration_id)
    else:
        # update old
        device.registration_id = registration_id
        device.mac_address = mac_address
        device.save()

    remote_device = RemoteDevice.objects.filter(device=device.id).first()
    if not remote_device:
        # create new
        RemoteDevice.objects.create(device=device, mac_address=mac_address)

    return HttpResponse(status.phrase, status=status.value)


@csrf_exempt
def vvm_test(request, *args, **kwargs):
    name = request.GET.get('name', 'ashish')
    if not name:
        status = HTTPStatus.BAD_REQUEST
        return HttpResponse(status.phrase, status=status.value)

    device = FCMDevice.objects.filter(name=name).first()
    if not device:
        status = HTTPStatus.BAD_REQUEST
        return HttpResponse(status.phrase, status=status.value)

    pnsType = request.GET.get('pnsType', 'VM')
    pnsSubType = request.GET.get('pnsSubType', 'VVM')

    data = {"nmsEventList": {"nmsEvent":
        [{"changedObject":

            {
                "parentFolder": "https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/folders/27a29814-dd8f-43ee-b768-19af98bf1d07",
                "resourceURL": "https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/objects/27a29814-dd8f-43ee-b768-19af98bf1d07%3A18",
                "flags": {"flag": ["\SEEN"]},
                "correlationId": "2020-09-25T14:46:35Z-conn:d3725318-b216be0a-13c4-65014-10e804a-216a34af-10e804a",
                "message": {"message-time": "2020-10-30T08:24:00-08:00",
                            "sender": "sip:14252081558@tmo.com",
                            "objectURL": "https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/objects/27a29814-dd8f-43ee-b768-19af98bf1d07%3A18",
                            "recipients": [{"uri": "tel:+12062912479"}],
                            "message-id": "2020-09-25T14:46:35Z-conn:d3725318-b216be0a-13c4-65014-10e804a-216a34af-10e804a",
                            "id": "18", "store": "VV-Mail/Inbox", "direction": "In",
                            "status": "SEEN"}}}]},
        "recipients": [{"uri": "tel:+12062912479"}],
        "channel": "", "pns-subtype": pnsSubType,
        "serviceName": "Sync App", "pns-type": pnsType
    }

    print(device.send_message(data={"push-message": data}))

    status = HTTPStatus.OK
    return HttpResponse(status.phrase, status=status.value)


@csrf_exempt
def api_run(request, *args, **kwargs):
    return HttpResponse('Success!')


class RemoteDeviceAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        device_id = data.get('device_id')
        registration_id = data.get('registration_id')
        device_type = data.get('type', 'android')
        mac_address = data.get('mac_address')
        name = data.get('name')
        is_new_device = False
        device = None

        if not mac_address:
            return Response({"message": "MAC address is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if device_id:
            device = FCMDevice.objects.filter(device_id=device_id).first()
            if not device and registration_id:
                is_new_device = True
                device = FCMDevice.objects.create(device_id=device_id, type=device_type,
                                                  registration_id=registration_id, name=name)
            else:
                device.registration_id = registration_id
                device.type = device_type
                device.name = name
                device.save()

        remote_device = RemoteDevice.objects.filter(mac_address=mac_address).first()
        if not remote_device:
            remote_device = RemoteDevice.objects.create(mac_address=mac_address, registration_date_time=timezone.now())
        else:
            remote_device.mac_address = mac_address
        if remote_device.device and is_new_device:
            remote_device.device.delete()
        if device:
            remote_device.device = device
        remote_device.save()

        return Response({"message": "Device registered successfully"},
                        status=status.HTTP_200_OK)


class VerifyDeviceAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        mac_address = request.query_params.get('mac_address', None)
        remote_device = RemoteDevice.objects.filter(mac_address=mac_address).first()
        if not remote_device:
            return Response({"message": "No Remote Device Found!"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            if remote_device.lock:
                response = {
                    "message": remote_device.note,
                    "lock": remote_device.lock,
                }
                return Response(response,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Device is active"},
                        status=status.HTTP_200_OK)


class CheckVersionAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        version_no = request.query_params.get('version_no', None)
        response = {
            "is_latest_version": True
        }
        app_versions = AppVersion.objects.all()
        latest_app_version = app_versions.first()
        current_app_version = app_versions.filter(version_no=version_no).first()
        if not current_app_version:
            return Response({"message": "Version Not Found"},
                            status=status.HTTP_400_BAD_REQUEST)
        if latest_app_version and current_app_version and latest_app_version != current_app_version and latest_app_version.id > current_app_version.id:
            response = AppVersionSerializer(instance=latest_app_version, context={"request": request}).data
            response.update(is_latest_version=False)
            return Response(response,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(response,
                        status=status.HTTP_200_OK)
