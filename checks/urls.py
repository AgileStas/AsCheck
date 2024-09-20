from django.urls import path
from django.views.generic import ListView

from . import views
from .models import Host, UsbStor

urlpatterns = [
    path("", views.index, name="index"),
    path("usbstor/", ListView.as_view(model=UsbStor), name="usbstors"),
    path("host/", ListView.as_view(model=Host), name="hosts"),
]
