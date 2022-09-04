from django.contrib import admin
from django.urls import path
from core import views as core_views


urlpatterns = [
    path('ping/', core_views.api_run),
    path('api/v1/device/register/', core_views.device_register),
    path('api/v1/download/updates/', core_views.download_updates),
    path('api/v1/check/updates/', core_views.check_updates),
    path('api/v1/vvm/test/', core_views.vvm_test),
]