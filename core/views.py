from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from http import HTTPStatus
from fcm_django.models import FCMDevice
from django.views.decorators.csrf import csrf_exempt
from .models import RemoteDevice
from django.conf import settings
from django.http import HttpResponse, Http404
import os
# Create your views here.

@csrf_exempt
def download_updates(request, *args, **kwargs):
    checksum = request.GET.get('checksum')
    if checksum:
        if len(checksum) == 33:
            file_path = settings.RAW_FILES_DIR+'/'+checksum
            if os.path.exists(file_path):
                 with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/pdf")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response

        file_path = settings.RAW_FILES_DIR+'/'+checksum
        print(file_path, "......Downloading")
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
    # status code
    status = HTTPStatus.OK

    device_id = request.POST.get('device_id')
    registration_id = request.POST.get('registration_id')
    type = request.POST.get('type', 'android')
    name = request.POST.get('name')

    if not device_id or not registration_id or not name or not type:
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
        device.save()

    remote_device = RemoteDevice.objects.filter(device=device.id).first()
    if not remote_device:
       # create new
       RemoteDevice.objects.create(device=device)

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

    data = {"nmsEventList":{"nmsEvent":
                                [{"changedObject":

        {"parentFolder":"https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/folders/27a29814-dd8f-43ee-b768-19af98bf1d07",
            "resourceURL":"https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/objects/27a29814-dd8f-43ee-b768-19af98bf1d07%3A18","flags":{"flag":["\SEEN"]},"correlationId":"2020-09-25T14:46:35Z-conn:d3725318-b216be0a-13c4-65014-10e804a-216a34af-10e804a",
            "message":{"message-time":"2020-10-30T08:24:00-08:00",
            "sender":"sip:14252081558@tmo.com",
            "objectURL":"https://wsg.t-mobile.com:443/phone20/mStoreRelay?path=http://wsg.mstore.msg.eng.t-mobile.com:8082/oemclient/nms/v1/ums/tel%3A%2B12062912479/objects/27a29814-dd8f-43ee-b768-19af98bf1d07%3A18","recipients":[{"uri":"tel:+12062912479"}],
            "message-id":"2020-09-25T14:46:35Z-conn:d3725318-b216be0a-13c4-65014-10e804a-216a34af-10e804a","id":"18","store":"VV-Mail/Inbox","direction":"In","status":"SEEN"}}}]},
            "recipients":[{"uri":"tel:+12062912479"}],
            "channel":"","pns-subtype":pnsSubType,
            "serviceName":"Sync App","pns-type":pnsType
            }

    print(device.send_message(data={"push-message": data}))

    status = HTTPStatus.OK
    return HttpResponse(status.phrase, status=status.value)

@csrf_exempt
def api_run(request, *args, **kwargs):
    return HttpResponse('Success!')