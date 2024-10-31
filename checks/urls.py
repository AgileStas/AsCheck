from django.urls import path
from django.views.generic import CreateView, ListView

from . import views
from .models import Division, Host, Person, UsbStor

urlpatterns = [
    path("", views.index, name="index"),
    path("division/", ListView.as_view(model=Division), name="divisions"),
    path("division/add", CreateView.as_view(model=Division, fields='__all__', success_url='.'), name="division_add"),
    path("host/", ListView.as_view(model=Host), name="hosts"),
    path("host/<int:pk>", views.HostUpdateView.as_view(), name="host_update"),
    path("host/upload", views.host_info_form, name="hostInfoUpload"),
    path("host/update/<cssiid>", views.host_update_info_form, name="hostInfoUpdate"),
    path("usbstor/", ListView.as_view(model=UsbStor), name="usbstors"),
    path("person/", ListView.as_view(model=Person), name="persons"),
    path("person/add", CreateView.as_view(model=Person, fields='__all__', success_url='.'), name="person_add"),
]
