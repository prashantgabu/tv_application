from django.urls import path
from rest_framework.routers import DefaultRouter

from core import views as core_views

router = DefaultRouter()
# router.register('election', views.ElectionViewSet, basename='election')


urlpatterns = [
                  path('remote_device/', core_views.RemoteDeviceAPIView.as_view(), name='remote_device'),
                  path('verify_device/', core_views.VerifyDeviceAPIView.as_view(), name='verify_device'),
                  path('check_version/', core_views.CheckVersionAPIView.as_view(), name='check_version'),
                  path('ping/', core_views.api_run),
                  path('device/register/', core_views.device_register),
                  path('download/updates/', core_views.download_updates),
                  path('check/updates/', core_views.check_updates),
                  path('vvm/test/', core_views.vvm_test),
              ] + router.urls
